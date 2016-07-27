
#pragma once

#include <iostream>

#include "queryset/models/model.h"
#include "types.h"
#include "informer.h"

namespace neutron {

    class WordUseManager;

    struct WordUseChoices {
        enum Choices { OK, NOT_ME, UNKNOWN, UNRECOGNIZED, NONE };
        WordUseChoices() : _choices(NONE) {}
        WordUseChoices(const Choices& c) : _choices(c) {}

        friend bool operator==(const WordUseChoices& lhs, const WordUseChoices& rhs) {
            return lhs._choices == rhs._choices;
        }

        friend bool operator<(const WordUseChoices& lhs, const WordUseChoices& rhs) {
            return lhs._choices < rhs._choices;
        }

        Choices _choices;
    };

    inline std::istream& operator >> (std::istream& is, WordUseChoices& w) {
        std::size_t token; is >> token;
        w._choices = static_cast<WordUseChoices::Choices>(token);
        return is;
    }
    std::ostream& operator << (std::ostream& os, const WordUseChoices& w);


    class WordUse : public qs::BaseModel<WordUse, Informer, std::size_t, std::string, float, meaning_id, WordUseChoices> {
        using BaseModel = qs::BaseModel<WordUse, Informer, std::size_t, std::string, float, meaning_id, WordUseChoices>;
        public:
            WordUse();
            WordUse(const BaseModel::tuple& data);
            virtual ~WordUse() {};

            virtual void print(std::ostream& os) const {
                os << "WordUse[" << pk() << "]";
            }

            // with a custom manager
            static WordUseManager& objects();
        };

    class WordUseManager : public BaseManager<WordUse> {
        public:
            WordUseManager();
    };

    template<class Ch, class Tr>
    std::basic_ostream<Ch, Tr>& operator<<(std::basic_ostream<Ch, Tr>& os, const neutron::WordUse& rhs) {
        rhs.print(os);
        return os;
    }
}
