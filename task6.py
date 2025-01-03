class Purrson:
    INITIAL_POCKET_SPACE = 1500
    INITIAL_CALORIES = 5000
    INITIAL_VIBE = "neutral"

    def __init__(self, name, food_dict):
      
        self.name = name
        self.pocket_space = Purrson.INITIAL_POCKET_SPACE
        self.pocket_content = []  
        self.calories = Purrson.INITIAL_CALORIES
        self.grid_positions = []
        self.vibe = Purrson.INITIAL_VIBE

      
        self.food_dictionary = food_dict

  
    def get_name(self):
        return self.name

    def get_pocket_space(self):
        return self.pocket_space

    def get_pocket_content(self):
        return self.pocket_content

    def get_calories(self):
        return self.calories

    def get_grid_positions(self):
        return self.grid_positions

    def get_vibe(self):
        return self.vibe

    def get_food_dictionary(self):
        return self.food_dictionary

 
    def update_calories_pocket_space(self, cal_change, space_change):
        
        self.calories = self.get_calories() + cal_change
        self.pocket_space = self.get_pocket_space() + space_change

    def update_pocket_content(self, food_item):
        
        self.get_pocket_content().append(food_item)

    def update_grid_position(self, new_position):
        
        self.get_grid_positions().append(new_position)

    def get_current_grid_position(self):
       
        if self.get_grid_positions():
            return self.get_grid_positions()[-1]
        return None

    def revert_state(self, n):
        for _ in range(n):
            if self.get_pocket_content():
                self.get_pocket_content().pop()
            if self.get_grid_positions():
                self.get_grid_positions().pop()

    def get_next_grid_positions(self, grid_dict):
        current_pos = self.get_current_grid_position()
        if current_pos is None:
            return []

        total_positions = len(grid_dict)
        N = 1
        while N * N < total_positions:
            N += 1

        top_right = N
        bottom_left = (N - 1) * N + 1
        top_left = 1
        bottom_right = N * N

        # 예외 처리: top_right or bottom_left
        if current_pos == top_right or current_pos == bottom_left:
            return sorted([top_left, bottom_right])

        # 기본 상하좌우 이동
        next_positions = []
        row = (current_pos - 1) // N
        col = (current_pos - 1) % N

        if row > 0:
            next_positions.append(current_pos - N)
        if row < N - 1:
            next_positions.append(current_pos + N)
        if col > 0:
            next_positions.append(current_pos - 1)
        if col < N - 1:
            next_positions.append(current_pos + 1)

        return sorted(next_positions)

    def display_pocket_content(self):
        pocket_codes = self.get_pocket_content()
        food_dict = self.get_food_dictionary()

        
        if not pocket_codes:
            print(f"+++ {self.get_name().upper()}'S POCKET CONTENT +++")
            print("No Food Items Consumed\n")
            print("+++ TOTAL NUTRITIONAL VALUES +++")
            print("Calories                   0 kcal")
            print("Carbohydrates              0 g")
            print("Fat                        0 g")
            print("Protein                    0 g")
            print("Sugars                     0 g")
            return

       
        valid_codes = [code for code in pocket_codes if code in food_dict]
        invalid_codes = [code for code in pocket_codes if code not in food_dict]

        if invalid_codes:
            print(f"Warning: The following food codes are invalid and will be skipped: {invalid_codes}")

        
        grouped_by_type = {}
        for code in valid_codes:
            ftype = food_dict[code]["Type"]
            if ftype not in grouped_by_type:
                grouped_by_type[ftype] = []
            grouped_by_type[ftype].append(code)

        print(f"+++ {self.get_name().upper()}'S POCKET CONTENT +++")

        
        total_nutrients = {
            "Calories": 0,
            "Carbohydrates": 0,
            "Fat": 0,
            "Protein": 0,
            "Sugars": 0
        }

        
        max_name_len = max((len(food_dict[code]["Food Name"]) for code in valid_codes), default=0)

        
        for category in sorted(grouped_by_type.keys()):
            print(category)
            print("No. " + "Food Name".ljust(max_name_len) + " Portion")

            for idx, code in enumerate(grouped_by_type[category], 1):
                fname = food_dict[code]["Food Name"]
                portion_str = f"{food_dict[code]['Portion']} g"
                print(f"[{idx}] {fname.ljust(max_name_len)} {portion_str.rjust(7)}")

                
                total_nutrients["Calories"] += food_dict[code]["Calories"]
                total_nutrients["Carbohydrates"] += food_dict[code]["Carbohydrates"]
                total_nutrients["Fat"] += food_dict[code]["Fat"]
                total_nutrients["Protein"] += food_dict[code]["Protein"]
                total_nutrients["Sugars"] += food_dict[code]["Sugars"]

            print()  

       
        print("+++ TOTAL NUTRITIONAL VALUES +++")
        print(f"Calories                 {total_nutrients['Calories']} kcal")
        print(f"Carbohydrates            {total_nutrients['Carbohydrates']} g")
        print(f"Fat                      {total_nutrients['Fat']} g")
        print(f"Protein                  {total_nutrients['Protein']} g")
        print(f"Sugars                   {total_nutrients['Sugars']} g")
        print()

    def met_win_conditions(self, win_condition):
        pocket_codes = self.get_pocket_content()
        food_dict = self.get_food_dictionary()

        valid_codes = [code for code in pocket_codes if code in food_dict]

        total_nutrients = {
            "Calories": 0,
            "Carbohydrates": 0,
            "Fat": 0,
            "Protein": 0,
            "Sugars": 0
        }

        for code in valid_codes:
            total_nutrients["Calories"] += food_dict[code]["Calories"]
            total_nutrients["Carbohydrates"] += food_dict[code]["Carbohydrates"]
            total_nutrients["Fat"] += food_dict[code]["Fat"]
            total_nutrients["Protein"] += food_dict[code]["Protein"]
            total_nutrients["Sugars"] += food_dict[code]["Sugars"]

        
        for nutrient, needed in win_condition.items():
            if total_nutrients.get(nutrient, 0) < needed:
                return False
        return True



class PurrsperityGrid(GameGrid):

    def __init__(self, grid_position, grid_dict, food_dict):
        super().__init__(grid_position, grid_dict, food_dict)

        # Overwrite some of the default settings
        self.set_food_type("Special Food")
        self.food_items = [
            "Double Pocket Space",
            "Replenish Calories",
            "Diminish Opponent's Calories",
            "Revert Opponent",
            "Double Last Food Item"
        ]

    def select_special_food_item(self, purrson, opponent):
       

       
        if not self.get_food_items():
            print(f"{self} has no more Special Food!\n")
            return

        
        print(self)
        for idx, item in enumerate(self.get_food_items(), start=1):
            print(f"[{idx}] {item}")
        print()

        choice_str = input("Select an item to consume: ")
        if not choice_str.isdigit():
            print("Invalid choice.\n")
            return
        
        choice = int(choice_str)
        if choice < 1 or choice > len(self.get_food_items()):
            print("Invalid choice.\n")
            return

       
        selected_item = self.get_food_items()[choice - 1]
        print(f"{purrson.get_name()} gains the ability to {selected_item}.\n")

  
        self.apply_special_effect(selected_item, purrson, opponent)

    
        self.remove_food_item(selected_item)

    def apply_special_effect(self, item, purrson, opponent):
        """
        Dispatch method to the correct effect function.
        """
        if item == "Double Pocket Space":
            self.effect_double_pocket_space(purrson)
        elif item == "Replenish Calories":
            self.effect_replenish_calories(purrson)
        elif item == "Diminish Opponent's Calories":
            self.effect_diminish_opponent(opponent)
        elif item == "Revert Opponent":
            self.effect_revert_opponent(purrson, opponent)
        elif item == "Double Last Food Item":
            self.effect_double_last_food_item(purrson)
        else:
            print("Unknown special item.\n")

   
    def effect_double_pocket_space(self, purrson):
        """
        Double the purrson's pocket_space.
        """
        current_space = purrson.get_pocket_space()
        purrson.update_calories_pocket_space(0, current_space)
        print(f"UPDATE: {purrson.get_vibe().capitalize()} {purrson.get_name()} now has "
              f"{purrson.get_pocket_space()} pocket space.\n")

    def effect_replenish_calories(self, purrson):
        """
        Set purrson's calories back to 5000.
        """
        current_cal = purrson.get_calories()
        needed_diff = 5000 - current_cal
        purrson.update_calories_pocket_space(needed_diff, 0)
        print(f"UPDATE: {purrson.get_vibe().capitalize()} {purrson.get_name()}'s calories is back to 5000.\n")

    def effect_diminish_opponent(self, opponent):
        """
        Halve the opponent's calories.
        """
        current_cal = opponent.get_calories()
        new_cal = current_cal // 2
        diff = new_cal - current_cal
        opponent.update_calories_pocket_space(diff, 0)
        print(f"UPDATE: {opponent.get_vibe().capitalize()} {opponent.get_name()}'s calories is down to {opponent.get_calories()}.\n")

    def effect_revert_opponent(self, purrson, opponent):
        """
        Prompt how many items/positions to revert (1..3).
        Then revert the opponent's state accordingly.
        Also adjust the opponent's calories/pocket_space.
        """
        revert_str = input("Select one option [1] Revert last 1 item, [2] last 2, [3] last 3: ")
        if not revert_str.isdigit():
            print("Invalid revert choice.\n")
            return

        revert_n = int(revert_str)
        if revert_n < 1 or revert_n > 3:
            print("Invalid revert number.\n")
            return

   
        items_to_remove = min(revert_n, len(opponent.get_pocket_content()))
        codes_removed = opponent.get_pocket_content()[-items_to_remove:]

    
        total_cal_removed = 0
        total_portion = 0
        food_dict = purrson.get_food_dictionary()  
        for code in codes_removed:
            if code in food_dict:
                total_cal_removed += food_dict[code]["Calories"]
                total_portion     += food_dict[code]["Portion"]
        opponent.revert_state(revert_n)

        
        opponent.update_calories_pocket_space(-total_cal_removed, total_portion)

        print(f"UPDATE: {opponent.get_vibe().capitalize()} {opponent.get_name()} items & positions have been reverted.\n")

    def effect_double_last_food_item(self, purrson):
        """
        purrson re-consumes the last item in pocket_content.
        """
        if not purrson.get_pocket_content():
            print("No items to double.\n")
            return

        last_code = purrson.get_pocket_content()[-1]
        food_dict = purrson.get_food_dictionary()
        if last_code not in food_dict:
            print("Invalid food code.\n")
            return

        cal = food_dict[last_code]["Calories"]
        portion = food_dict[last_code]["Portion"]

        
        purrson.update_pocket_content(last_code)


        purrson.update_calories_pocket_space(cal, -portion)

        print(f"UPDATE: {purrson.get_vibe().capitalize()} {purrson.get_name()} just doubled the last item.\n")



if __name__ == "__main__":
    # Example usage
    grid = {
        1: {}, 2: {}, 3: {},
        4: {}, 5: {}, 6: {},
        7: {}, 8: {}, 9: {},
        10: {}, 11: {}, 12: {},
        13: {}, 14: {}, 15: {},
        16: {}
    }

    # Suppose you have Purrson class from Task 3 or Task 4:
    # For demonstration, we'll define a minimal mock Purrson class here
    class Purrson:
        INITIAL_POCKET_SPACE = 1500
        INITIAL_CALORIES = 5000
        INITIAL_VIBE = "neutral"

        def __init__(self, name, food_dict):
            self.name = name
            self.calories = Purrson.INITIAL_CALORIES
            self.pocket_space = Purrson.INITIAL_POCKET_SPACE
            self.pocket_content = []
            self.grid_positions = []
            self.vibe = Purrson.INITIAL_VIBE
            self.food_dictionary = food_dict

        def get_name(self):
            return self.name

        def get_vibe(self):
            return self.vibe

        def get_calories(self):
            return self.calories

        def get_pocket_space(self):
            return self.pocket_space

        def get_pocket_content(self):
            return self.pocket_content

        def get_food_dictionary(self):
            return self.food_dictionary

        def update_calories_pocket_space(self, cal_change, space_change):
            # cal_change can be + or -
            self.calories += cal_change
            # space_change can be + or -
            self.pocket_space += space_change

        def update_pocket_content(self, food_code):
            self.pocket_content.append(food_code)

        def update_grid_position(self, new_pos):
            self.grid_positions.append(new_pos)

        def revert_state(self, n):
            for _ in range(n):
                if self.pocket_content:
                    self.pocket_content.pop()
                if self.grid_positions:
                    self.grid_positions.pop()

  


