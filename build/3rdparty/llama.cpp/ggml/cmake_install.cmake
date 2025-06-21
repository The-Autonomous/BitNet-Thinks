# Install script for directory: F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "C:/Program Files (x86)/bitnet.cpp")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("F:/CalebCode/2025/Bitnet/build/3rdparty/llama.cpp/ggml/src/cmake_install.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "F:/CalebCode/2025/Bitnet/build/3rdparty/llama.cpp/ggml/src/ggml.lib")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "F:/CalebCode/2025/Bitnet/build/bin/ggml.dll")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE FILE FILES
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-alloc.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-backend.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-blas.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-cann.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-cuda.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-kompute.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-metal.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-rpc.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-sycl.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-vulkan.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-bitnet.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "F:/CalebCode/2025/Bitnet/build/3rdparty/llama.cpp/ggml/src/ggml.lib")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "F:/CalebCode/2025/Bitnet/build/bin/ggml.dll")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE FILE FILES
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-alloc.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-backend.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-blas.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-cann.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-cuda.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-kompute.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-metal.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-rpc.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-sycl.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-vulkan.h"
    "F:/CalebCode/2025/Bitnet/3rdparty/llama.cpp/ggml/include/ggml-bitnet.h"
    )
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
if(CMAKE_INSTALL_LOCAL_ONLY)
  file(WRITE "F:/CalebCode/2025/Bitnet/build/3rdparty/llama.cpp/ggml/install_local_manifest.txt"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
endif()
