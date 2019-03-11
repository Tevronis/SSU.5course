#include <iostream>
#include <string>
#include <algorithm>
#include <fstream>
#include <vector>
#include <direct.h>
#include <assert.h>
#include <stdio.h>
#include "utils.h"
#include "drive_serial.h"
#include "md5.h"


using namespace std;

typedef unsigned char byte;


int find_in_bytefile(vector<int> &v, string s) {
    vector<int> sb = string_to_vector_int(std::move(s));
    bool first = true;
    for(int pos = 0; pos < v.size(); pos++) {
        bool flag = true;
        for(int j = 0; j < sb.size(); j++) {
            if (v[pos + j] != sb[j]) {
                flag = false;
                break;
            }
        }
        if (flag && !first) {
            return pos;
        }
        if (flag)
            first = false;
    }
    return -1;
}

int get_config_possible_len(vector<int> &f, int start) {
    /* config_system[result] */

    int pos = start + 14;
    std::stringstream stream;
    int c = string_to_vector_int("]")[0];
    while (f[pos] != c) {
        stream << f[pos] - 48;
        pos += 1;
    }

    std::string result( stream.str() );
    return string_to_int(result);
}

int get_config_start_to_write(vector<int> &f, int start) {
    int pos = start + 14;
    int c = string_to_vector_int("]")[0];
    while (f[pos] != c)
        pos += 1;
    return pos;
}

int set_string_to_config(vector<int> &byte_file, string s) {
    int pos = find_in_bytefile(byte_file, "config_system");
    int len = get_config_possible_len(byte_file, pos);
    assert(s.size() < len);
    pos = get_config_start_to_write(byte_file, pos) + 1;
    for(int i = 0; i < s.size(); i++) {
        byte_file[pos + i] = s[i];
    }
    return pos;
}


void set_string_to_overhead(vector<int> &byte_file, string s) {
    for (char item : s) {
        byte_file.push_back(item);
    }
}


vector<string> get_overhead_params(vector<int> &byte_file) {
    vector<string> result;
    string conf;
    for (int i = byte_file.size() - (4 * 32 + 4); i < byte_file.size(); i++) {
        int x = byte_file[i];
        conf += char(x);
    }
    result = split(conf, '|');
    //result.pop_back();
    return result;
}


vector<string> get_system_params(const string &filename, const string &filename2, bool contain_overhead=false) {
    vector<string> result;
    result.push_back(get_filename(filename2));
    if (contain_overhead)
        result.push_back(int_to_string(get_file_size(filename) - (4 * 32 + 4)));
    else
        result.push_back(int_to_string(get_file_size(filename)));

    vector<int> file_without_config = read_file(filename);
    string to_hash;
    if (contain_overhead) {
        for (int i = 0; i < file_without_config.size() - (32 * 4 + 4); i++)
            to_hash += int_to_string(file_without_config[i]);
    }
    else {
        for (int item : file_without_config)
            to_hash += int_to_string(item);
    }
    MD5 md5 = MD5();
    result.emplace_back(md5.digestString(const_cast<char *>(to_hash.c_str())));

    string drive_name = get_current_drive_name();
    LPCTSTR serial;
    GetPhysicalDriveSerialNumber(serial, drive_name);
    result.emplace_back(serial);

    return result;
}

vector<string> get_config_params(vector<int> &byte_file) {
    vector<string> result;
    int pos = find_in_bytefile(byte_file, "config_system");
    int len = get_config_possible_len(byte_file, pos);
    pos = get_config_start_to_write(byte_file, pos) + 1;
    string conf;
    for (int i = pos; i < pos + len; i++) {
        int x = byte_file[i];
        conf += char(x);
    }
    result = split(conf, '|');
    result.pop_back();
    return result;
}

int main(int argc, char* argv[]) {
    vector<int> f = read_file(argv[0]);
    if (f[f.size() - 1] != 124) {
        vector<string> system_params;
        char * create_program_filename;
        if (argc > 1)
            create_program_filename = argv[1];
        else
            create_program_filename = const_cast<char *>(argv[0]);
        system_params = get_system_params(argv[0], create_program_filename);
        string to_set;
        MD5 md5 = MD5();
        for (const string &s: system_params) {
            to_set += md5.digestString(const_cast<char *>(s.c_str()));
            to_set += "|";
            cout << to_set << endl;
        }
        set_string_to_overhead(f, to_set);
        const char * ff = "program.exe";
        write_file_deep(ff, f);
        ofstream myfile;
        myfile.open("1.bat");
        myfile << "timeout 5\ndel " << get_filename(argv[0]) << "\nrename program.exe " << get_filename(argv[0]) << "\ndel 1.bat";
        myfile.close();
        ShellExecute ( NULL, NULL, "1.bat", NULL, NULL, SW_SHOWNORMAL );
    } else {
        vector<string> config_params = get_overhead_params(f);
        vector<string> system_params;
        system_params = get_system_params(argv[0], argv[0], true);

        MD5 md5 = MD5();

        /*for (const auto &config_param : config_params) {
            cout << config_param << " ";
        }
        cout << endl;
        for (const auto &system_param : system_params) {
            cout << system_param << " ";
        }
        cout << endl;*/
        if (system_params.size() != config_params.size()) {
            cout << "Incorrect count of system params" << endl;
            system("pause");
            exit(0);
        }
        bool flag = false;
        for (int i = 0; i < system_params.size(); i++) {
            cout << md5.digestString(const_cast<char *>(system_params[i].c_str())) << " " << config_params[i] << endl;
            if (md5.digestString(const_cast<char *>(system_params[i].c_str())) != config_params[i]) {
                if (i == 0)
                    cout << "Incorrect filename" << endl;
                if (i == 1)
                    cout << "Incorrect filesize" << endl;
                if (i == 2)
                    cout << "Incorrect hash(file)" << endl;
                if (i == 3)
                    cout << "Incorrect drive serial" << endl;
                flag = true;
            }
        }
        if (flag) {
            system("pause");
            exit(0);
        }
        cout << "good finish" << endl;
        system("pause");
    }
}
