# CMAKE generated file: DO NOT EDIT!
# Generated by "MinGW Makefiles" Generator, CMake Version 3.12

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

SHELL = cmd.exe

# The CMake executable.
CMAKE_COMMAND = "C:\Program Files\JetBrains\CLion 2018.2.1\bin\cmake\win\bin\cmake.exe"

# The command to remove a file.
RM = "C:\Program Files\JetBrains\CLion 2018.2.1\bin\cmake\win\bin\cmake.exe" -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = C:\Users\Mike\PycharmProjects\SSU.5course\task2

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = C:\Users\Mike\PycharmProjects\SSU.5course\task2\cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/installer.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/installer.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/installer.dir/flags.make

CMakeFiles/installer.dir/main.cpp.obj: CMakeFiles/installer.dir/flags.make
CMakeFiles/installer.dir/main.cpp.obj: ../main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=C:\Users\Mike\PycharmProjects\SSU.5course\task2\cmake-build-debug\CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/installer.dir/main.cpp.obj"
	C:\Programs\MinGW\bin\g++.exe  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles\installer.dir\main.cpp.obj -c C:\Users\Mike\PycharmProjects\SSU.5course\task2\main.cpp

CMakeFiles/installer.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/installer.dir/main.cpp.i"
	C:\Programs\MinGW\bin\g++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E C:\Users\Mike\PycharmProjects\SSU.5course\task2\main.cpp > CMakeFiles\installer.dir\main.cpp.i

CMakeFiles/installer.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/installer.dir/main.cpp.s"
	C:\Programs\MinGW\bin\g++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S C:\Users\Mike\PycharmProjects\SSU.5course\task2\main.cpp -o CMakeFiles\installer.dir\main.cpp.s

# Object files for target installer
installer_OBJECTS = \
"CMakeFiles/installer.dir/main.cpp.obj"

# External object files for target installer
installer_EXTERNAL_OBJECTS =

installer.exe: CMakeFiles/installer.dir/main.cpp.obj
installer.exe: CMakeFiles/installer.dir/build.make
installer.exe: CMakeFiles/installer.dir/linklibs.rsp
installer.exe: CMakeFiles/installer.dir/objects1.rsp
installer.exe: CMakeFiles/installer.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=C:\Users\Mike\PycharmProjects\SSU.5course\task2\cmake-build-debug\CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable installer.exe"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles\installer.dir\link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/installer.dir/build: installer.exe

.PHONY : CMakeFiles/installer.dir/build

CMakeFiles/installer.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles\installer.dir\cmake_clean.cmake
.PHONY : CMakeFiles/installer.dir/clean

CMakeFiles/installer.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "MinGW Makefiles" C:\Users\Mike\PycharmProjects\SSU.5course\task2 C:\Users\Mike\PycharmProjects\SSU.5course\task2 C:\Users\Mike\PycharmProjects\SSU.5course\task2\cmake-build-debug C:\Users\Mike\PycharmProjects\SSU.5course\task2\cmake-build-debug C:\Users\Mike\PycharmProjects\SSU.5course\task2\cmake-build-debug\CMakeFiles\installer.dir\DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/installer.dir/depend
