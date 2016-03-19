
#include <iostream>
#include <boost/program_options.hpp>
#include <boost/filesystem.hpp>

#include "neutron/informer.h"


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
        neutron::Informer::informer_vector_type informers;
        fs::path informers_file = path / "data_informers.tsv";
        neutron::Informer::parse(informers_file.string(), informers);
        
        for (auto& informer : informers) {
            std::cout << std::get<0>(informer) << " - " << std::get<1>(informer) << "\n";
        }
    }
    catch(std::exception& e) {
        std::cerr << "Unhandled Exception reached the top of main: " 
            << e.what() << ", application will now exit" << std::endl; 
            return -1; 
    }
    return 0;

}