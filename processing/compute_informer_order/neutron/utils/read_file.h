
#pragma once

#include <fstream>
#include <tuple>

namespace neutron {
    namespace utils {
        
        // Credit: http://stackoverflow.com/questions/14033828/translating-a-stdtuple-into-a-template-parameter-pack
        //  - [BUG]: Initializator list order: http://stackoverflow.com/questions/14060264/order-of-evaluation-of-elements-in-list-initialization
        namespace {
            template <typename T>
            struct _helper_caster {
                _helper_caster(std::istream& ss) { ss >> _dato;};
                operator T() {return std::move(_dato);}
                T _dato;
            };            
        }
        
        template<typename... Args>
        std::tuple<Args...> parse(std::stringstream& stream) {            
            return std::tuple<Args...> { _helper_caster<Args>(stream)... };
        }
        
        template<typename... Args>
        void read_file(const std::string& filename, std::vector<std::tuple<Args...>>& data) {
            std::ifstream infile(filename);
            
            std::string line;
            while (std::getline(infile, line)) {
                if (line.compare(0, 1, "#") != 0) {
                    data.push_back(parse<Args...>(std::stringstream(line)));
                }
            }
        }
        
    }
}