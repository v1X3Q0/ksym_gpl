cmake_minimum_required(VERSION 3.5.0)
project(SV_GPL)

set(SV_GPL sv_gpl.h)
add_custom_command(
    OUTPUT ${SV_GPL}
    COMMAND python3 ${CMAKE_CURRENT_SOURCE_DIR}/gplsym_list.py --sv_store ${CMAKE_CURRENT_SOURCE_DIR}/svstore.txt --header ${CMAKE_CURRENT_BINARY_DIR}/${SV_GPL}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
)
add_custom_target(ksym_gpl ALL DEPENDS ${SV_GPL})

file(GLOB ConfigFiles ${CMAKE_CURRENT_SOURCE_DIR}/svstore.txt)

add_custom_target(copy)
foreach(ConfigFile ${ConfigFiles})
  add_custom_command(TARGET copy PRE_BUILD
                     COMMAND ${CMAKE_COMMAND} -E
                         copy ${ConfigFile} ${CMAKE_CURRENT_BINARY_DIR}/svstore.txt)
endforeach()
