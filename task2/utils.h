#include <utility>

//
// Created by Mike on 05.10.2018.
//

#ifndef TASK2_UTILS_H
#define TASK2_UTILS_H
#include <iostream>
#include <string>
#include <algorithm>
#include <fstream>
#include <vector>
#include <sstream>
#include <assert.h>
#include <winnt.h>
#include <windef.h>
#include <afxres.h>
//#include <ntsecapi.h>
//#include <ddk/winddk.h>
//#include <winternl.h>
//#include "ntstatus.h"
//#include <ntddk.h>

using namespace std;

typedef unsigned char byte;

bool cmdOptionExists(char** begin, char** end, const std::string& option) {
    return std::find(begin, end, option) != end;
}

vector<int> read_file(const string &path) {
    vector<int> result;
    std::ifstream is(path, std::ifstream::binary);
    if (is) {
        // get length of file:
        is.seekg(0, std::ifstream::end);
        int length = int(is.tellg());
        is.seekg(0, std::ifstream::beg);

        char * buffer = new char[length];

        is.read(buffer, length);
        is.close();

        for (int i = 0; i < length; i++) {
            byte b = byte(buffer[i]);
            result.push_back(b);
        }

        delete[] buffer;
    }
    return result;
}

/*NTSTATUS TestDelZwSetInformationFile(IN HANDLE  FileHandle,
                                     OUT PIO_STATUS_BLOCK  IoStatusBlock,
                                     IN PVOID  FileInformation,
                                     IN ULONG  Length,
                                     IN FILE_INFORMATION_CLASS  FileInformationClass)
{
    NTSTATUS ntstatus = STATUS_SUCCESS;

    if (FileInformationClass==FileDispositionInformation) {//delete
        PFILE_OBJECT    FileObject = NULL;

        ObReferenceObjectByHandle( FileHandle, 0, NULL, KernelMode, &FileObject, NULL );
        if ( FileObject ) {
#ifdef DBG
            DbgPrint("Deleting %ws", FileObject->FileName.Buffer);
#endif

            //zero ImageSection - теперь можно будет удалить образ любого выполняющегося exe в системе
            if (FileObject->SectionObjectPointer->ImageSectionObject)
                FileObject->SectionObjectPointer->ImageSectionObject= 0;

            ObDereferenceObject(FileObject);
        }
    }

    //calling original handler
    ntstatus = RealZwSetInformationFile(FileHandle,    IoStatusBlock, FileInformation,    Length,    FileInformationClass);

#ifdef DBG
    if (FileInformationClass==FileDispositionInformation) //delete
        //по умолчанию для выполняющегося exe - ntstatus = STATUS_CANNOT_DELETE
        //в нашем случае для выполняющегося exe - ntstatus = STATUS_SUCCESS и
        //файл exe успешно удаляется драйвером файл. системы
        DbgPrint("TestDel, TestDelZwSetInformationFile  status= 0x%08X", ntstatus);
#endif

    return ntstatus;
}*/

void write_file_deep(const char *filename, vector<int> &bytes) {
    //::GetFileSecurityA(TEXT("installer.exe"), NULL, NULL, NULL, NULL);
    HANDLE file = ::CreateFile(TEXT(filename), GENERIC_READ | GENERIC_WRITE, 0,
                               NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if(INVALID_HANDLE_VALUE == file)
        cout <<  ::GetLastError();

    int SIZE = bytes.size();
    char *mass = new char[bytes.size()];
    for (int i = 0; i < bytes.size(); i++) {
        mass[i] = byte(bytes[i]);
    }

    DWORD dwNumberOfBytesWritten;
    WriteFile(file, (LPCVOID)mass, SIZE * sizeof(char), &dwNumberOfBytesWritten, NULL);

    CloseHandle(file);
}

string string_to_hex(string &s) {
    std::stringstream ss;
    for (char c : s)
        ss << std::hex << (int) c;
    std::string result = ss.str();
    return result;
}

string int_to_hex(int d) {
    std::stringstream stream;
    stream << std::hex << d;
    std::string result( stream.str() );
    return result;
}

vector<int> string_to_vector_int(string h) {
    vector<int> result;
    for(char c: h)
        result.push_back(int(c));
    return result;
}

int string_to_int(const string &s) {
    return std::stoi(s);
}

string int_to_string(int d) {
    return  std::to_string(d);
}

string MBFromW(LPCWSTR pwsz, UINT cp) {
    int cch = WideCharToMultiByte(cp, 0, pwsz, -1, 0, 0, NULL, NULL);

    char* psz = new char[cch];

    WideCharToMultiByte(cp, 0, pwsz, -1, psz, cch, NULL, NULL);

    std::string st(psz);
    delete[] psz;

    return st;
}

int get_file_size(const string &filename) {
    std::ifstream in(filename, std::ifstream::ate | std::ifstream::binary);
    return static_cast<int>(in.tellg());
}

vector<string> split(string s, char sep=' ') {
    vector<string> result;
    string temp;
    for (char chr : s) {
        if (chr == sep) {
            result.push_back(temp);
            temp = "";
            continue;
        }
        temp += chr;
    }
    if (temp != "")
        result.push_back(temp);
    return result;
}

string get_filename(string path) {
    vector<string> s = split(std::move(path), '\\');
    return s.back();
}

string get_current_drive_name() {
    char current_work_dir[FILENAME_MAX];
    _getcwd(current_work_dir, sizeof(current_work_dir));
    // std::cout << "\t" << current_work_dir << endl;
    string path(current_work_dir);
    vector<string> s = split(std::move(path), '\\');
    return s.front();
}



#endif //TASK2_UTILS_H
