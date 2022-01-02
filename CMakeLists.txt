set(SV_GPL sv_gpl.h)
add_custom_command(
    OUTPUT ${SV_GPL}
    COMMAND python3 ${CMAKE_CURRENT_SOURCE_DIR}/gplsym_list.py --sv_store ${CMAKE_CURRENT_SOURCE_DIR}/svstore.txt --header ${CMAKE_CURRENT_BINARY_DIR}/${SV_GPL}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
)
add_custom_target(ksym_gpl ALL DEPENDS ${SV_GPL})
