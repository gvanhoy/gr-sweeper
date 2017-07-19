INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_SWEEPER sweeper)

FIND_PATH(
    SWEEPER_INCLUDE_DIRS
    NAMES sweeper/api.h
    HINTS $ENV{SWEEPER_DIR}/include
        ${PC_SWEEPER_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    SWEEPER_LIBRARIES
    NAMES gnuradio-sweeper
    HINTS $ENV{SWEEPER_DIR}/lib
        ${PC_SWEEPER_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(SWEEPER DEFAULT_MSG SWEEPER_LIBRARIES SWEEPER_INCLUDE_DIRS)
MARK_AS_ADVANCED(SWEEPER_LIBRARIES SWEEPER_INCLUDE_DIRS)

