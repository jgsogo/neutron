
#include "word_use.h"

#include <boost/filesystem.hpp>
#include <spdlog/spdlog.h>
#include <spdlog/fmt/ostr.h>

#include "manager.h"
#include "config_store.h"
#include "entropy.h"


namespace neutron {

    namespace {
        std::string word_use_path() {
            namespace fs = boost::filesystem;
            auto word_use_filename = ConfigStore::get().get_value_as<std::string>("files/worduse_data");
            fs::path full_path = ConfigStore::get().get_value_as<std::string>("db_path") / fs::path(word_use_filename);
            return full_path.string();
        }
    }

    WordUseManager::WordUseManager() : BaseManager<WordUse>(word_use_path()) {}

    std::vector<std::pair<meaning_id, float>> WordUseManager::gather_entropy_data(const std::vector<Informer>& informers) {
        auto log = spdlog::get("neutron");

        auto data = WordUse::objects().all().filter<Informer>(informers);
        log->debug(" - data: {} samples.", data.count());

        // Compute entropy
        std::vector<std::pair<meaning_id, float>> entropy_data; // TODO: Initialize with size
        for (auto meaning: data.groupBy<meaning_id>()) {
            log->debug("   + meaning {}", meaning.first);
            // Initialize counts with at least one observation of each variable
            std::map<WordUseChoices, std::size_t> counts = {{WordUseChoices(WordUseChoices::OK), 1},
                                                            {WordUseChoices(WordUseChoices::NOT_ME), 1},
                                                            {WordUseChoices(WordUseChoices::UNKNOWN), 1},
                                                            {WordUseChoices(WordUseChoices::UNRECOGNIZED), 1}};
            for (auto choice: meaning.second.groupBy<WordUseChoices>()) {
                log->debug("     - {}: {}", choice.first, choice.second.count());
                counts[choice.first] = choice.second.count();
            }
            auto entropy = utils::compute_entropy(counts);
            entropy_data.push_back(std::make_pair(meaning.first, entropy));
            log->debug("   => {}", entropy);
            log->info("   + meaning {}: {}", meaning.first, entropy);
        }
        return entropy_data;
    }


    std::ostream& operator << (std::ostream& os, const WordUseChoices& w) {
        switch(w._choices) {
            case WordUseChoices::OK: return os << "Ok";
            case WordUseChoices::NOT_ME: return os << "Not me";
            case WordUseChoices::UNKNOWN: return os << "Unknown";
            case WordUseChoices::UNRECOGNIZED: return os << "Unrecognized";
            default: return os << "None(" << w._choices << ")";
        }
    }



    WordUse::WordUse() {
    }
    WordUse::WordUse(const BaseModel::tuple& data) : WordUse::BaseModel(data) {
    }

    WordUseManager& WordUse::objects() {
        static WordUseManager manager;
        return manager;
    }

}
