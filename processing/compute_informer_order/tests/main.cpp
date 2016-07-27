#define BOOST_TEST_MODULE "Test Neutron Basic"
#include <boost/test/unit_test.hpp>
#include "spdlog/spdlog.h"
#include <iostream>

#include "../neutron/config_store.h"
#include "config_tests.h"

struct GlobalConfig {
    GlobalConfig() {
        std::cout << "global setup\n";
        #ifdef SPDLOG_DEBUG_ON
            auto console = spdlog::stdout_logger_mt("neutron");
            auto qs = spdlog::stdout_logger_mt("qs");
            qs->set_level(spdlog::level::debug);
            console->set_level(spdlog::level::debug);
            console->info("Logging Neutron: test neutron basic");
        #endif
    
        std::string data = "{\"db_path\": \"" + test_data_dir.string() + "\", \"files\": { \"informers_data\" : \"informers.tsv\", \"region\": \"regions.tsv\"}}";
        neutron::ConfigStore::get().parse_data(data);        
    }

    ~GlobalConfig() {
        std::cout << "global teardown\n";
    }
};

BOOST_GLOBAL_FIXTURE(GlobalConfig);
