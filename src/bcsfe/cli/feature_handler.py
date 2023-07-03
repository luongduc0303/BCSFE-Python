from typing import Any, Callable, Optional
from bcsfe.core import io, locale_handler
from bcsfe.cli import dialog_creator, color, basic_items, save_management


class FeatureHandler:
    def __init__(self, save_file: "io.save.SaveFile"):
        self.save_file = save_file

    def get_features(self):
        features: dict[str, Any] = {
            "save_management": {
                "save_save": save_management.SaveManagement.save_save,
                "save_upload": save_management.SaveManagement.save_upload,
                "save_save_file": save_management.SaveManagement.save_save_dialog,
                "adb_push": save_management.SaveManagement.adb_push,
                "adb_push_rerun": save_management.SaveManagement.adb_push_rerun,
                "export_save": save_management.SaveManagement.export_save,
                "unban_account": save_management.SaveManagement.unban_account,
            },
            "items": {
                "catfood": basic_items.BasicItems.edit_catfood,
                "xp": basic_items.BasicItems.edit_xp,
                "normal_tickets": basic_items.BasicItems.edit_normal_tickets,
                "rare_tickets": basic_items.BasicItems.edit_rare_tickets,
                "platinum_tickets": basic_items.BasicItems.edit_platinum_tickets,
                "legend_tickets": basic_items.BasicItems.edit_legend_tickets,
                "platinum_shards": basic_items.BasicItems.edit_platinum_shards,
                "np": basic_items.BasicItems.edit_np,
                "leadership": basic_items.BasicItems.edit_leadership,
                "catamins": basic_items.BasicItems.edit_catamins,
                "catseyes": basic_items.BasicItems.edit_catseyes,
                "catfruit": basic_items.BasicItems.edit_catfruit,
            },
        }
        return features

    def get_feature(self, feature_name: str):
        feature_path = feature_name.split(".")
        feature_dict = self.get_features()
        feature = feature_dict
        for path in feature_path:
            feature = feature[path]

        return feature

    def search_features(
        self,
        name: str,
        parent_path: str = "",
        features: Optional[dict[str, Any]] = None,
        found_features: Optional[set[str]] = None,
    ) -> set[str]:
        name = name.lower().replace(" ", "")
        if features is None:
            features = self.get_features()
        if found_features is None:
            found_features = set()

        for feature_name_key, feature in features.items():
            feature_name = locale_handler.LocalManager().get_key(feature_name_key)
            path = (
                f"{parent_path}.{feature_name_key}" if parent_path else feature_name_key
            )
            if isinstance(feature, dict):
                found_features.update(
                    self.search_features(
                        name,
                        path,
                        feature,  # type: ignore
                        found_features,
                    )
                )
            elif name in feature_name.lower().replace(" ", "") or name == "":
                found_features.add(path)

        return found_features

    def display_features(self, features: list[str]):
        feature_names: list[str] = []
        for feature_name in features:
            feature_names.append(feature_name.split(".")[-1])
        print()
        dialog_creator.ListOutput(feature_names, [], "features", {}).display_locale()

    def select_features(self, features: list[str], parent_path: str = "") -> list[str]:
        if features != list(self.get_features().keys()):
            features.insert(0, "go_back")
        self.display_features(features)
        print()
        usr_input = color.ColoredInput().localize("select_features")
        selected_features: list[str] = []
        if usr_input.isdigit():
            usr_input = int(usr_input)
            if usr_input > len(features):
                color.ColoredText.localize("invalid_input")
            elif usr_input < 1:
                color.ColoredText.localize("invalid_input")
            else:
                feature_name_top = features[usr_input - 1]
                if feature_name_top == "go_back":
                    return list(self.get_features().keys())
                feature = self.get_feature(feature_name_top)
                if isinstance(feature, dict):
                    for feature_name in feature.keys():
                        feature_path = (
                            f"{parent_path}.{feature_name_top}.{feature_name}"
                            if parent_path
                            else f"{feature_name_top}.{feature_name}"
                        )
                        selected_features.append(feature_path)

                else:
                    feature_path = (
                        f"{parent_path}.{feature}" if parent_path else feature
                    )
                    selected_features.append(feature_path)

        else:
            selected_features = list(self.search_features(usr_input))

        return selected_features

    def select_features_run(self):
        features = self.get_features()
        features = list(features.keys())
        while True:
            features = self.select_features(features)
            feature = None
            if len(features) == 1:
                feature = features[0]
            if len(features) == 2 and features[0] == "go_back":
                feature = features[1]

            if feature:
                if isinstance(feature, Callable):
                    feature(self.save_file)
                    features = self.get_features()
                    features = list(features.keys())
                else:
                    feature = self.get_feature(feature)
                    if isinstance(feature, Callable):
                        feature(self.save_file)
                        features = self.get_features()
                        features = list(features.keys())