
#include <iostream>
#include <boost/program_options.hpp>
#include <boost/filesystem.hpp>
#include <boost/algorithm/string/join.hpp>

#include <spdlog/spdlog.h>
#include <spdlog/fmt/ostr.h>

#include "log_level_param.hpp"
#include "neutron/config_store.h"
#include "neutron/informer.h"
#include "neutron/region.h"
#include "neutron/word_use.h"
#include "neutron/word_coarse.h"

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

template <typename T>
void work_model(const std::vector<Informer>& informers, const boost::filesystem::path& fullpath);

int main(int argc, char** argv){
    std::cout << "== Compute informer order ==\n";
    try {
        // Define and parse the program options
        namespace po = boost::program_options;
        po::options_description desc("Options");
        desc.add_options() 
          ("help", "Print help messages")
          ("log-level,l", po::value<log_level>()->default_value(log_level(spdlog::level::info)), std::string("log level (" + log_level::options() + ")").c_str())
          ("settings", po::value<std::string>()->required(), "path to settings file")
          ("outpath", po::value<std::string>()->required(), "output path (last directory will be created if not exists)")
          ("game", po::value<std::string>()->required(), "game: WordUse or WordCoarse");  // TODO: Make choices
 
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
        
        // Get logger level (initialize also child loggers)
        spdlog::level::level_enum log_level = vm["log-level"].as<::log_level>()._level;
        //#ifdef SPDLOG_DEBUG_ON
        spdlog::stdout_logger_mt("qs")->set_level(log_level);
        //#endif
        auto console = spdlog::stdout_logger_mt("neutron");
        console->set_level(log_level);

        // Get settings
        namespace fs = boost::filesystem;
        fs::path settings = vm["settings"].as<std::string>();
        std::cout << " - path to settings: '" << settings << "'\n";
        console->info("Configure Neutron: '{}'", settings);
        ConfigStore::get().parse_file(settings.string());

        // Get game:
        fs::path game = vm["game"].as<std::string>();

        // Prepare output path
        fs::path outpath = vm["outpath"].as<std::string>();
        std::cout << " - output path: '" << outpath << "'\n";
        try {
            create_directory(outpath);
        }
        catch (fs::filesystem_error& e) {
            std::cerr << "Cannot access/create directory'" << outpath.string() << "': " << e.what() << ".\n";
        }

        std::cout << "== List of informers ==" << std::endl;
        auto informers = Informer::objects().all();
        for (auto& region : informers.groupBy<Region>(false)) {
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

            if (game=="WordUse") {
                std::ostringstream os; os << "worduse_region_" << region.first.pk() << ".tsv";
                work_model<WordUse>(informers, outpath / fs::path(os.str()));
            }
            else if (game=="WordCoarse") {
                std::ostringstream os; os << "wordcoarse_region_" << region.first.pk() << ".tsv";
                work_model<WordCoarse>(informers, outpath / fs::path(os.str()));
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


template <typename T>
void work_model(const std::vector<Informer>& informers, const boost::filesystem::path& fullpath) {
    std::vector<std::pair<meaning_id, float>> entropy_data = T::objects().gather_entropy_data(informers);
    std::sort(entropy_data.begin(), entropy_data.end(),
              [](const std::pair<meaning_id, float>& lhs, const std::pair<meaning_id, float>& rhs) {
                    return lhs.second > rhs.second; // Reverse order.
              });

    // Write to file
    std::ofstream ofs; ofs.open(fullpath.string());
    for (auto& item: entropy_data) {
        ofs << item.first << "\t" << item.second << "\n";
    }
    ofs.close();
}
