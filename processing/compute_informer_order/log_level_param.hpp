
#pragma once

#include <boost/program_options.hpp>
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

    static std::string options() {
        std::ostringstream s;
        std::copy(spdlog::level::level_names,
            spdlog::level::level_names + spdlog::level::off + 1,
            std::ostream_iterator<std::string>(s, ", "));
        return s.str().substr(0, s.str().length() - 2);
        //std::string log_level_help = "log level (" + s.str().substr(0, s.str().length() - 2) + ")";
    }
    spdlog::level::level_enum _level;
};

std::ostream& operator << (std::ostream& os, const log_level& level) {
    os << spdlog::level::to_str(level._level);
    return os;
}


std::istream& operator >> (std::istream& is, log_level& level) {
    std::string token; is >> token;
    std::size_t idx = _detail::index_of(spdlog::level::level_names, spdlog::level::level_names + spdlog::level::off + 1, token.c_str());
    if (idx > spdlog::level::off) {
        throw boost::program_options::validation_error(boost::program_options::validation_error::invalid_option_value);
    }
    level._level = static_cast<spdlog::level::level_enum>(idx);
    return is;
}
