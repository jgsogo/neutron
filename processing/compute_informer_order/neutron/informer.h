
#pragma once

#include "utils/read_file.h"

namespace neutron {
    class Informer {
        public:
            typedef std::vector<std::tuple<std::size_t, std::size_t>> informer_vector_type;
        
            static std::size_t parse(const std::string& filename, informer_vector_type& informers) {
                std::size_t old_length = informers.size();
                utils::read_file<std::size_t, std::size_t>(filename, informers);
                return informers.size() - old_length;
            }
        protected:
    };
}