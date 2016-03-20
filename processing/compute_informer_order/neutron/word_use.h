
#pragma once

#include "utils/base_manager.h"

namespace neutron {
    class WordUseManager : public utils::BaseManager<std::size_t,
                                                     std::size_t,
                                                     std::size_t,
                                                     std::size_t,
                                                     std::size_t> {
    public:
        typedef std::map<std::size_t, std::vector<std::tuple<std::size_t, std::size_t, std::size_t, std::size_t>>> worduse_by_interface_type;

    public:
        WordUseManager(const std::string& filename) : BaseManager(filename) {
            /*
            for (auto& item : _raw_data) {
                const std::size_t& first = std::get<0>(item);
                const std::size_t& second = std::get<1>(item);
                _all.insert(std::make_pair(first, second));
                _all_by_region[first].push_back(second);
            }
            */
        }

    protected:
        worduse_by_interface_type _all_by_interface;
    };
}
