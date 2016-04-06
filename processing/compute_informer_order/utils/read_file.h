
#pragma once

#include <fstream>
#include <tuple>
#include <vector>
#include <string>
#include <sstream>

namespace utils {
        
    // Reference: http://stackoverflow.com/questions/14033828/translating-a-stdtuple-into-a-template-parameter-pack
    //  - [BUG]: Initializator list order: http://stackoverflow.com/questions/14060264/order-of-evaluation-of-elements-in-list-initialization
    //  - Maybe improve with: http://stackoverflow.com/questions/10014713/build-tuple-using-variadic-templates
    namespace {
        template <typename T>
        T read(std::istream& is) {
            T t; is >> t; return t;
        }
    }
        
    template<typename... Args>
    std::tuple<Args...> parse(std::istream& stream) {            
        return std::tuple<Args...> { read<Args>(stream)... };
    }
        
    template<typename... Args>
    void read_file(const std::string& filename, std::vector<std::tuple<Args...>>& data) {
        std::ifstream infile(filename);
            
        std::string line;
        while (std::getline(infile, line)) {
            if (line.compare(0, 1, "#") != 0) {
                data.push_back(parse<Args...>(std::istream(line)));
            }
        }
    }
        
}
