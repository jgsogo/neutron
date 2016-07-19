
#include <iostream>
#include <boost/program_options.hpp>
#include <boost/filesystem.hpp>
#include <boost/algorithm/string/join.hpp>

#include "spdlog/spdlog.h"

#include "log_level_param.hpp"
#include "neutron/config_store.h"
#include "neutron/informer.h"
#include "neutron/region.h"
#include "neutron/word_use.h"

#include "entropy.h"

using namespace neutron;

template <class Iter>
std::ostream& implode(Iter first, Iter last, std::ostream& os, const std::string& sep = ", ") {
    if (first != last) {
        --last;
        while (first != last) {
            os << *first << sep;
            ++first;
        }
        os << *last;
    }
    return os;
}

int main(int argc, char** argv){
    std::cout << "== Compute informer order ==\n";
    try {
        // Define and parse the program options
        namespace po = boost::program_options;
        po::options_description desc("Options");
        desc.add_options() 
          ("help", "Print help messages")
          ("log-level,l", po::value<log_level>()->default_value(log_level(spdlog::level::info)), std::string("log level (" + log_level::options() + ")").c_str())
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
        
        // Get logger level
        spdlog::level::level_enum log_level = vm["log-level"].as<::log_level>()._level;
        #ifdef SPDLOG_DEBUG_ON
        spdlog::stdout_logger_mt("qs")->set_level(log_level);
        #endif
        auto console = spdlog::stdout_logger_mt("neutron");
        console->set_level(log_level);

        // Get settings
        namespace fs = boost::filesystem;
        fs::path settings = vm["settings"].as<std::string>();
        std::cout << " - path to settings: '" << settings << "'\n";
        console->info("Configure Neutron: '{}'", settings);
        ConfigStore::get().parse_file(settings.string());

        std::cout << "== List of informers ==" << std::endl;
        auto informers = Informer::objects().all();
        for (auto& region : informers.groupBy<Region>()) {
            std::cout << region.first << ":" << std::endl;
            for (auto& informer : region.second) {
                std::cout << "\t- " << informer << std::endl;
            }
        }

        std::cout << "== Compute entropy for each region ==" << std::endl;
        for (auto& region : Informer::objects().all().groupBy<Region>()) {
            auto informers_ = region.second.value_list<informer_id>();
            std::vector<Informer> informers(informers_.begin(), informers_.end());
            std::cout << region.first << ": ";
            implode(informers.begin(), informers.end(), std::cout);
            std::cout << std::endl;

            // Data associated with the informers
            auto data = WordUse::objects().all().filter<Informer>(informers);
            std::cout << " - data: " << data.count() << " samples." << std::endl;

            for (auto meaning: data.groupBy<meaning_id>()) {
                std::cout << "   + meaning " << meaning.first << std::endl;
                // Initialize counts with at least one observation of each variable
                std::map<WordUseChoices, std::size_t> counts = {{WordUseChoices(WordUseChoices::OK), 1},
                                                                {WordUseChoices(WordUseChoices::NOT_ME), 1},
                                                                {WordUseChoices(WordUseChoices::UNKNOWN), 1},
                                                                {WordUseChoices(WordUseChoices::UNRECOGNIZED), 1}};
                for (auto choice: meaning.second.groupBy<WordUseChoices>()) {
                    std::cout << "     - " << choice.first << ": " << choice.second.count() << std::endl;
                    counts[choice.first] = choice.second.count();
                }
                std::cout << "   => " << utils::compute_entropy(counts) << std::endl;
            }

            for (auto choice : data.groupBy<WordUseChoices>()) {
                std::cout << "   + " << choice.first << ": " << choice.second.count() << std::endl;
            }
        }
    }
    catch(std::exception& e) {
        std::cerr << "Unhandled Exception reached the top of main: " 
            << e.what() << ", application will now exit" << std::endl; 
            return -1; 
    }
    return 0;

}
