
#pragma once

#include <iostream>

#include "queryset/models/model.h"
#include "types.h"
#include "informer.h"


namespace neutron {

    class WordCoarseManager;

    struct WordCoarseData {
        WordCoarseData() {}
        WordCoarseData(const bool& c) : _coarse(c) {}

        friend bool operator==(const WordCoarseData& lhs, const WordCoarseData& rhs) {
            return lhs._coarse == rhs._coarse;
        }

        friend bool operator<(const WordCoarseData& lhs, const WordCoarseData& rhs) {
            return lhs._coarse < rhs._coarse;
        }

        bool _coarse;
    };

    inline std::istream& operator >> (std::istream& is, WordCoarseData& w) {
        std::string token; is >> token;
        w._coarse = (token == "TRUE");
        return is;
    }
    std::ostream& operator << (std::ostream& os, const WordCoarseData& w);

    class WordCoarse : public qs::BaseModel<WordCoarse, Informer, std::size_t, std::string, float, meaning_id, WordCoarseData> {
        using BaseModel = qs::BaseModel<WordCoarse, Informer, std::size_t, std::string, float, meaning_id, WordCoarseData>;
        public:
            WordCoarse();
            WordCoarse(const BaseModel::tuple& data);
            virtual ~WordCoarse() {};

            virtual void print(std::ostream& os) const {
                os << "WordCoarse[" << pk() << "]";
            }

            // with a custom manager
            static WordCoarseManager& objects();
        };

    class WordCoarseManager : public BaseManager<WordCoarse> {
        public:
            WordCoarseManager();
            std::vector<std::pair<meaning_id, float>> gather_entropy_data(const std::vector<Informer>& informers);
    };

    template<class Ch, class Tr>
    std::basic_ostream<Ch, Tr>& operator<<(std::basic_ostream<Ch, Tr>& os, const neutron::WordCoarse& rhs) {
        rhs.print(os);
        return os;
    }

}
