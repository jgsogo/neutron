
#include <iostream>
#include <boost/program_options.hpp>
#include <boost/filesystem.hpp>

#include "spdlog/spdlog.h"

#include "neutron/config_store.h"
#include "neutron/informer.h"
#include "neutron/region.h"
#include "neutron/word_use.h"

#include "queryset/queryset.h"

using namespace neutron;

int main(int argc, char** argv){
    #ifdef SPDLOG_DEBUG_ON
    spdlog::stdout_logger_mt("qs")->set_level(spdlog::level::debug);
    #endif
    auto console = spdlog::stdout_logger_mt("neutron");
    console->set_level(spdlog::level::debug);

    std::cout << "== Compute informer order ==\n";
    try {
        // Define and parse the program options
        namespace po = boost::program_options;
        po::options_description desc("Options");
        desc.add_options() 
          ("help", "Print help messages") 
          ("settings", po::value<std::string>()->required(), "path to settings file");
 
        po::variables_map vm;
        try {
            po::store(po::parse_command_line(argc, argv, desc), vm); // can throw
            // handle help option
            if(vm.count("help")) { 
                std::cout << "Basic Command Line Parameter App" << std::endl 
                          << desc << std::endl; 
                return 0; 
            }
            po::notify(vm); // throws on error, so do after help in case there are any problems             
        }
        catch(po::error& e) {
            std::cerr << "ERROR: " << e.what() << std::endl << std::endl; 
            std::cerr << desc << std::endl; 
            return -1; 
        }
        
        namespace fs = boost::filesystem;
        fs::path settings = vm["settings"].as<std::string>();
        std::cout << " - path to settings: '" << settings << "'\n";
        console->info("Configure Neutron: '{}'", settings);
        ConfigStore::get().parse_file(settings.string());

        auto informers = Informer::objects().all();
        auto by_region = informers.groupBy<region_id>().get();
        for (auto& region : by_region) {
            auto local_informers = region.second.value_list<informer_id>();
        }

        /*
        // Parse informers
        fs::path informers_file = path / "data_informers.tsv";
        neutron::InformerManager informers(informers_file.string());

        // Parse worduse
        fs::path word_use_file = path / "data_worduse.tsv";
        neutron::WordUseManager word_uses(word_use_file.string());

        // == Play a little bit with the data
        std::cout << "Get all spaniards (region_id = 1)" << std::endl;
        auto spaniards = informers.get_by_region(neutron::region_id(1));
        for (auto& item : spaniards) {
            std::cout << item << std::endl;
        }
        std::cout << "Get all spaniards (region_id = 1) -- version 2" << std::endl;
        auto spaniards2 = ::utils::list<neutron::informer_id>(informers.filter(neutron::region_id(1)));
        for (auto& item : spaniards2) {
            std::cout << item << std::endl;
        }
        */
        /*
        auto word_use_data_all = word_uses.all();

        auto spaniards_data = word_uses.filter(spaniards);
        for (auto& item : spaniards_data) {
            std::cout << item << std::endl;
        }
        */

        // == Play with querysets
        //QuerySet<neutron::informer_id, neutron::region_id> qs(informers.all());
        //qs.filter(neutron::region_id(1));
    }
    catch(std::exception& e) {
        std::cerr << "Unhandled Exception reached the top of main: " 
            << e.what() << ", application will now exit" << std::endl; 
            return -1; 
    }
    return 0;

}