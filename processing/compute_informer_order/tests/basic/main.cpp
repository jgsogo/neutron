#define BOOST_TEST_MODULE "Test Neutron Basic"
#define BOOST_TEST_NO_MAIN
#include <boost/test/unit_test.hpp>
#include "spdlog/spdlog.h"

// entry point:
int main(int argc, char* argv[])
{
    #ifdef SPDLOG_DEBUG_ON
        auto console = spdlog::stdout_logger_mt("neutron");
        auto qs = spdlog::stdout_logger_mt("qs");
        qs->set_level(spdlog::level::debug);
        console->set_level(spdlog::level::debug);
        console->info("Logging Neutron: test neutron basic");
    #endif

    return boost::unit_test_framework::unit_test_main(init_unit_test, argc, argv);
}