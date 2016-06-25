
#pragma once

//#include <boost/program_options.hpp>
#include <boost/algorithm/string/predicate.hpp>
#include "spdlog/common.h"

namespace _detail {
    template <typename Iter>
    std::size_t index_of(Iter first, Iter last, typename const std::iterator_traits<Iter>::value_type& x)
    {
        std::size_t i = 0;
        while (first != last && !boost::iequals(*first, x))
            ++first, ++i;
        return i;
    }
}

struct log_level {
    log_level() : _level(spdlog::level::info) {}
    log_level(const spdlog::level::level_enum& level) : _level(level) { }
    log_level(const log_level& other) : _level(other._level) {}

    spdlog::level::level_enum _level;
};

std::ostream& operator << (std::ostream& os, const log_level& level) {
    os << level._level;
    return os;
}


std::istream& operator >> (std::istream& is, log_level& level) {
    std::string token; is >> token;
    std::size_t idx = _detail::index_of(spdlog::level::level_names, spdlog::level::level_names + spdlog::level::off + 1, token.c_str());
    level._level = static_cast<spdlog::level::level_enum>(idx);
    return is;
}


/*
namespace spdlog {
    namespace level {
        std::ostream& operator<<(std::ostream& os, const level_enum& level) {
            os << spdlog::level::to_str(level);
            return os;
        }

        std::istream& operator>>(std::istream& iss, level_enum& level) {
            std::size_t aux;
            iss >> aux;
            level = static_cast<level_enum>(aux);
            return iss;
        }
    }
}
*/




void validate(boost::any& v, std::vector<std::string> const& values, spdlog::level::level_enum* /* target_type */, int) {
    namespace po = boost::program_options;

    // Make sure no previous assignment to 'v' was made.
    po::validators::check_first_occurrence(v);

    // Extract the first string from 'values'. If there is more than
    // one string, it's an error, and exception will be thrown.
    const std::string& s = po::validators::get_single_string(values);

    std::size_t x = _detail::index_of(spdlog::level::level_names, spdlog::level::level_names + spdlog::level::off, s.c_str());
    
    v = boost::any(log_level(static_cast<spdlog::level::level_enum>(x)));
    /*
    if (s == "cat" || s == "dog") {
        v = boost::any(catdog(s));
    }
    else {
        throw validation_error(validation_error::invalid_option_value);
    }
    */
}
