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

using namespace std;

typedef unsigned char byte;

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

void write_file(const string &path, vector<int> bytes) {
    std::ofstream of(path, std::ifstream::binary);

    char * ww = new char[bytes.size()];

    for (int i = 0; i < bytes.size(); i++)
        ww[i] = byte(bytes[i]);

    of.write(ww, (int)bytes.size());
    delete[] ww;
    of.close();
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

string get_drive_name(string path) {
    vector<string> s = split(std::move(path), '\\');
    return s.front();
}



#endif //TASK2_UTILS_H
