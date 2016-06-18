
#pragma once

#include "types.h"

namespace neutron {
    /*
    class WordUseManager : public ::utils::BaseManager<informer_id,
                                                       interface_id,
                                                       meaning_id,
                                                       int,
                                                       word_id> {
    public:
        typedef std::map<interface_id, std::vector<std::tuple<informer_id, meaning_id, int, word_id>>> worduse_by_interface_type;

    public:
        WordUseManager(const std::string& filename) : BaseManager(filename) {
            for (auto& item : _raw_data) {
                const interface_id& interface = std::get<1>(item);
                auto data = ::utils::tuple::project<0, 2, 3, 4>(item);
                _all_by_interface[interface].push_back(data);
            }
        }

    protected:
        worduse_by_interface_type _all_by_interface;
    };
    */
}
