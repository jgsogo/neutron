
#pragma once

#include <iostream>

#include "queryset/models/model.h"
#include "types.h"
#include "informer.h"


namespace neutron {

    class WordAlternateManager;

    class WordAlternate : public qs::BaseModel<WordAlternate, Informer, std::size_t, std::string, float, meaning_id, word_id> {
        using BaseModel = qs::BaseModel<WordAlternate, Informer, std::size_t, std::string, float, meaning_id, word_id>;
        public:
            WordAlternate();
            WordAlternate(const BaseModel::tuple& data);
            virtual ~WordAlternate() {};

            virtual void print(std::ostream& os) const {
                os << "WordAlternate[" << pk() << "]";
            }

            // with a custom manager
            static WordAlternateManager& objects();
        };

    class WordAlternateManager : public BaseManager<WordAlternate> {
        public:
            WordAlternateManager();
            std::vector<std::pair<meaning_id, float>> gather_entropy_data(const std::vector<Informer>& informers);
    };

    template<class Ch, class Tr>
    std::basic_ostream<Ch, Tr>& operator<<(std::basic_ostream<Ch, Tr>& os, const neutron::WordAlternate& rhs) {
        rhs.print(os);
        return os;
    }

}
