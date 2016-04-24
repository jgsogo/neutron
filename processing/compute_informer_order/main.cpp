
#include <iostream>
#include <boost/program_options.hpp>
#include <boost/filesystem.hpp>

#include "neutron/informer.h"
#include "neutron/word_use.h"

#include "models/queryset.h"


int main(int argc, char** argv){
    std::cout << "== Compute informer order ==\n";
    try {
        // Define and parse the program options
        namespace po = boost::program_options;
        po::options_description desc("Options");
        desc.add_options() 
          ("help", "Print help messages") 
          ("path", po::value<std::string>()->required(), "path to files");
 
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
        fs::path path = vm["path"].as<std::string>();
        std::cout << " - path to files: '" << path << "'\n";
        
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