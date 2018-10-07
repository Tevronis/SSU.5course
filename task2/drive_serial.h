//
// Created by Mike on 07.10.2018.
//

#ifndef TASK2_DRIVE_SERIAL_H
#define TASK2_DRIVE_SERIAL_H


#include <iostream>
#include <windows.h>
#include <cstring>
#include <commctrl.h>
#include <winioctl.h>
#include <tchar.h>
#include <vector>

using namespace std;

#define IOCTL_STORAGE_QUERY_PROPERTY   CTL_CODE(IOCTL_STORAGE_BASE, 0x0500, METHOD_BUFFERED, FILE_ANY_ACCESS)

typedef enum _STORAGE_PROPERTY_ID {
    StorageDeviceProperty                   = 0,
    StorageAdapterProperty,
    StorageDeviceIdProperty,
    StorageDeviceUniqueIdProperty,
    StorageDeviceWriteCacheProperty,
    StorageMiniportProperty,
    StorageAccessAlignmentProperty,
    StorageDeviceSeekPenaltyProperty,
    StorageDeviceTrimProperty,
    StorageDeviceWriteAggregationProperty,
    StorageDeviceDeviceTelemetryProperty,
    StorageDeviceLBProvisioningProperty,
    StorageDevicePowerProperty,
    StorageDeviceCopyOffloadProperty,
    StorageDeviceResiliencyProperty,
    StorageDeviceMediumProductType,
    StorageDeviceIoCapabilityProperty       = 48,
    StorageAdapterProtocolSpecificProperty,
    StorageDeviceProtocolSpecificProperty,
    StorageAdapterTemperatureProperty,
    StorageDeviceTemperatureProperty,
    StorageAdapterPhysicalTopologyProperty,
    StorageDevicePhysicalTopologyProperty,
    StorageDeviceAttributesProperty
} STORAGE_PROPERTY_ID, *PSTORAGE_PROPERTY_ID;

typedef enum _STORAGE_QUERY_TYPE {
    PropertyStandardQuery    ,
    PropertyExistsQuery      ,
    PropertyMaskQuery        ,
    PropertyQueryMaxDefined
} STORAGE_QUERY_TYPE, *PSTORAGE_QUERY_TYPE;

typedef struct _STORAGE_PROPERTY_QUERY {
    STORAGE_PROPERTY_ID PropertyId;
    STORAGE_QUERY_TYPE  QueryType;
    BYTE                AdditionalParameters[1];
} STORAGE_PROPERTY_QUERY, *PSTORAGE_PROPERTY_QUERY;

typedef struct _STORAGE_DESCRIPTOR_HEADER {
    DWORD Version;
    DWORD Size;
} STORAGE_DESCRIPTOR_HEADER, *PSTORAGE_DESCRIPTOR_HEADER;

typedef struct _STORAGE_DEVICE_DESCRIPTOR {
    DWORD            Version;
    DWORD            Size;
    BYTE             DeviceType;
    BYTE             DeviceTypeModifier;
    BOOLEAN          RemovableMedia;
    BOOLEAN          CommandQueueing;
    DWORD            VendorIdOffset;
    DWORD            ProductIdOffset;
    DWORD            ProductRevisionOffset;
    DWORD            SerialNumberOffset;
    STORAGE_BUS_TYPE BusType;
    DWORD            RawPropertiesLength;
    BYTE             RawDeviceProperties[1];
} STORAGE_DEVICE_DESCRIPTOR, *PSTORAGE_DEVICE_DESCRIPTOR;


DWORD GetPhysicalDriveSerialNumber(LPCTSTR & strSerialNumber OUT, string &path)
{
    DWORD dwRet = NO_ERROR;

    string dev = R"(\\.\)" + path;
    LPCSTR dev_l = dev.c_str();
    // cout << "disk: " << dev_l << endl;

    // Format physical drive path (may be '\\.\PhysicalDrive0', '\\.\PhysicalDrive1' and so on).

    // Get a handle to physical drive
    HANDLE hDevice = ::CreateFile(TEXT(dev_l), 0, FILE_SHARE_READ | FILE_SHARE_WRITE,
                                  NULL, OPEN_EXISTING, 0, NULL);

    if(INVALID_HANDLE_VALUE == hDevice)
        return ::GetLastError();

    // Set the input data structure
    STORAGE_PROPERTY_QUERY storagePropertyQuery;
    ZeroMemory(&storagePropertyQuery, sizeof(STORAGE_PROPERTY_QUERY));
    storagePropertyQuery.PropertyId = StorageDeviceProperty;
    storagePropertyQuery.QueryType = PropertyStandardQuery;

    // Get the necessary output buffer size
    STORAGE_DESCRIPTOR_HEADER storageDescriptorHeader = {0};
    DWORD dwBytesReturned = 0;
    if(! ::DeviceIoControl(hDevice, IOCTL_STORAGE_QUERY_PROPERTY,
                           &storagePropertyQuery, sizeof(STORAGE_PROPERTY_QUERY),
                           &storageDescriptorHeader, sizeof(STORAGE_DESCRIPTOR_HEADER),
                           &dwBytesReturned, NULL))
    {
        dwRet = ::GetLastError();
        ::CloseHandle(hDevice);
        return dwRet;
    }

    // Alloc the output buffer
    const DWORD dwOutBufferSize = storageDescriptorHeader.Size;
    BYTE* pOutBuffer = new BYTE[dwOutBufferSize];
    ZeroMemory(pOutBuffer, dwOutBufferSize);

    // Get the storage device descriptor
    if(! ::DeviceIoControl(hDevice, IOCTL_STORAGE_QUERY_PROPERTY,
                           &storagePropertyQuery, sizeof(STORAGE_PROPERTY_QUERY),
                           pOutBuffer, dwOutBufferSize,
                           &dwBytesReturned, NULL))
    {
        dwRet = ::GetLastError();
        delete []pOutBuffer;
        ::CloseHandle(hDevice);
        return dwRet;
    }

    // Now, the output buffer points to a STORAGE_DEVICE_DESCRIPTOR structure
    // followed by additional info like vendor ID, product ID, serial number, and so on.
    STORAGE_DEVICE_DESCRIPTOR* pDeviceDescriptor = (STORAGE_DEVICE_DESCRIPTOR*)pOutBuffer;
    const DWORD dwSerialNumberOffset = pDeviceDescriptor->SerialNumberOffset;
    if(dwSerialNumberOffset != 0)
    {
        // Finally, get the serial number
        strSerialNumber = LPCTSTR(pOutBuffer + dwSerialNumberOffset);
    }

    // Do cleanup and return
    delete []pOutBuffer;
    ::CloseHandle(hDevice);
    return dwRet;
}


#endif //TASK2_DRIVE_SERIAL_H
