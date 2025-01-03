def acquire_food(food_options_file, ingredients_file):
    def round_float(value):
        return round(value, 4)

    # Read ingredients data
    ingredients_data = {}
    with open(ingredients_file, 'r') as ingrfile:
        lines = ingrfile.readlines()
        delimiter = ';' if ';' in lines[0] else '/'  # Detect delimiter
        for line in lines[1:]:  # Skip the header
            parts = line.strip().split(delimiter)
            if len(parts) == 6:
                if delimiter == ';':  # Ingredients2
                    ingredients_data[parts[5].strip()] = {
                        'Calories': float(parts[1]),
                        'Carbohydrates': float(parts[3]),
                        'Sugars': float(parts[0]),
                        'Protein': float(parts[4]),
                        'Fat': float(parts[2])
                    }
                elif delimiter == '/':  # Ingredients1
                    ingredients_data[parts[0].strip()] = {
                        'Calories': float(parts[1]),
                        'Carbohydrates': float(parts[2]),
                        'Sugars': float(parts[3]),
                        'Protein': float(parts[4]),
                        'Fat': float(parts[5])
                    }

    # Read food options and calculate nutritional values
    food_data = {}
    with open(food_options_file, 'r') as foodfile:
        lines = foodfile.readlines()
        delimiter = '|' if '|' in lines[0] else '-'  # Detect delimiter
        header = lines[0].strip().split(delimiter)  # Parse header to determine column indices

        for line in lines[1:]:  # Skip the header
            parts = line.strip().split(delimiter)
            if len(parts) == len(header):
                # Extract values using header indices
                code = parts[header.index('Code')].strip()
                food_name = parts[header.index('Food Name')].strip()
                portion = int(parts[header.index('Portion (g)')].strip())
                main_ingredients = parts[header.index('Main Ingredients (Top 3)')].strip().split(',')
                food_type = parts[header.index('Type')].strip()

                # Calculate nutritional values
                percentages = [0.4, 0.25, 0.15]
                totals = {'Calories': 0, 'Carbohydrates': 0, 'Sugars': 0, 'Protein': 0, 'Fat': 0}

                for i in range(len(main_ingredients)):
                    ingredient = main_ingredients[i].strip()
                    if ingredient in ingredients_data:
                        percentage = percentages[i]
                        factor = portion * percentage / 100
                        totals['Calories'] += ingredients_data[ingredient]['Calories'] * factor
                        totals['Carbohydrates'] += ingredients_data[ingredient]['Carbohydrates'] * factor
                        totals['Sugars'] += ingredients_data[ingredient]['Sugars'] * factor
                        totals['Protein'] += ingredients_data[ingredient]['Protein'] * factor
                        totals['Fat'] += ingredients_data[ingredient]['Fat'] * factor

                food_data[code] = {
                    'Food Name': food_name,
                    'Type': food_type,
                    'Portion': portion,
                    'Calories': round_float(totals['Calories']),
                    'Carbohydrates': round_float(totals['Carbohydrates']),
                    'Sugars': round_float(totals['Sugars']),
                    'Protein': round_float(totals['Protein']),
                    'Fat': round_float(totals['Fat'])
                }

    return food_data
class GameGrid:
    """
    A class representing a single cell/position in an NxN grid.
    """

    # Class Variables
    INITIAL_VIBE = "neutral"
    # Alphabetical order for the two food types found in Task 2
    FOOD_TYPE_LIST = ["Decadent Dessert", "Healthy Treats"]  # "D" < "H" so this is alphabetical

    def __init__(self, grid_position, grid_dict, food_dict):
        """
        Constructor for a single grid cell in an NxN game grid.

        :param grid_position: (int) The integer position of this grid cell (1..N*N).
        :param grid_dict: (dict) The game grid dictionary from Task 1 (keys: 1..N*N).
        :param food_dict: (dict) The dictionary of foods from Task 2.
        """

        # 1) Set up instance variables
        self.grid_position = grid_position           # the integer position of the grid
        self.food_type     = "No Food Type"          # string representing the type of food
        self.food_items    = []                      # list of food codes stored in this grid
        self.vibe          = GameGrid.INITIAL_VIBE   # string representing the vibe of the grid

        # Determine the dimension N of the grid (assume square)
        # len(grid_dict) is the total number of positions, so N = sqrt(len(grid_dict))
        total_positions = len(grid_dict)
        # A simple approach if you know the grid is always square:
        # e.g., for 9 positions => N=3, for 16 => N=4, etc.
        # (No imports allowed, so let's do an integer approach)
        N = 1
        while N * N < total_positions:
            N += 1

        # Identify special positions (top-right, bottom-left, middle if N is odd).
        top_right_pos   = N
        bottom_left_pos = (N - 1) * N + 1
        middle_pos      = (N * N + 1) // 2 if (N % 2 == 1) else None

        # 2) Decide whether this position is a "skip" (i.e. no food)
        #    or whether we assign Decadent Dessert / Healthy Treats
        is_skip = (self.grid_position == top_right_pos) or \
                  (self.grid_position == bottom_left_pos) or \
                  (middle_pos is not None and self.grid_position == middle_pos)

        # Only if not skip, decide which food type based on checkerboard pattern:
        #   if (row+col) is even => "Decadent Dessert", else => "Healthy Treats"
        if not is_skip:
            # figure out row, col in 0-based indexing
            row = (self.grid_position - 1) // N
            col = (self.grid_position - 1) % N
            if (row + col) % 2 == 0:
                self.set_food_type("Decadent Dessert")
            else:
                self.set_food_type("Healthy Treats")

            # 3) Generate a list of food items from the food_dict matching self.food_type
            #    If "Decadent Dessert", gather all codes of that type
            #    If "Healthy Treats", gather all codes of that type
            #    If "No Food Type", skip
            matched_codes = []
            for code, info in food_dict.items():
                if info["Type"] == self.get_food_type():
                    matched_codes.append(code)
            self.food_items = matched_codes

        # 4) Add this GameGrid object into the grid dictionary under the key "grid object".
        grid_dict[self.grid_position]["grid object"] = self

    # ----------------------------------------------------------------
    # Getter Methods
    # ----------------------------------------------------------------
    def get_grid_position(self):
        return self.grid_position

    def get_food_type(self):
        return self.food_type

    def get_food_items(self):
        return self.food_items

    def get_vibe(self):
        return self.vibe

    # ----------------------------------------------------------------
    # Grid Update & Other Retrieval Methods
    # ----------------------------------------------------------------
    def set_food_type(self, new_food_type):
        """
        Updates the food type of the grid.
        """
        self.food_type = new_food_type

    def add_food_item(self, food_item_code):
        """
        Add a single food code to this grid's food_items list.
        """
        self.food_items.append(food_item_code)

    def remove_food_item(self, food_item_code):
        """
        Remove a single food code from this grid's food_items list if it exists.
        """
        if food_item_code in self.food_items:
            self.food_items.remove(food_item_code)

    def display_food_items(self, food_dict, pocket_space):
        """
        Prints no more than 5 food items in self.food_items whose 'Portion' <= pocket_space.
        Format specification:
         Position X: <FOOD TYPE> Grid [Y Food Items Available]
         If no items fit => "No Food Items fit Pocket Space"
         Otherwise => 
           No. Food Name              Portion
           [1] somefoodname           100 g
           [2] ...
           ...
        The portion column must be right-aligned, with 1 space after the longest Food Name.
        """

        # Print the heading line
        position_str  = f"Position {self.get_grid_position()}"
        food_type_str = self.get_food_type()
        items_count   = len(self.get_food_items())
        print(f"{position_str}: {food_type_str} Grid [{items_count} Food Items Available]")

        # Filter out items whose portion <= pocket_space
        valid_items = []
        for code in self.get_food_items():
            portion = food_dict[code]["Portion"]
            if portion <= pocket_space:
                valid_items.append(code)

        if len(valid_items) == 0:
            print("No Food Items fit Pocket Space")
            return

        # Display up to 5 of those items
        valid_items = valid_items[:5]

        # Find the longest food name among these valid items
        max_name_len = 0
        for code in valid_items:
            name_len = len(food_dict[code]["Food Name"])
            if name_len > max_name_len:
                max_name_len = name_len

        # Print header line
        # The "Portion" column should start 1 space after the longest Food Name
        # We'll build the format string accordingly
        print_str = "No. " + "Food Name".ljust(max_name_len) + " "
        print_str += "Portion"
        print(print_str)

        # Print each item
        count = 1
        for code in valid_items:
            food_name = food_dict[code]["Food Name"]
            portion   = food_dict[code]["Portion"]
            # Right-align the portion in a field, e.g. if portion is 3 digits, ensure it lines up
            # We can simply use str.rjust(...) to line it up
            # But we first figure out how many characters the portion column should have
            # For a simpler approach, we can do something like 5 or 6 spaces, or just right-justify in 4
            # We'll do a small calc: since "Portion" is 7 letters, let's ensure we have enough space
            portion_str = str(portion) + " g"
            # We'll place portion_str so it begins after the 1 space following the longest name
            line = f"[{count}] " + food_name.ljust(max_name_len) + " " + portion_str.rjust(len("Portion"))
            print(line)
            count += 1

    # ----------------------------------------------------------------
    # String Representation
    # ----------------------------------------------------------------
    def __str__(self):
        """
        Return "Position <GRID POSITION>: <FOOD TYPE> Grid [<NUMBER> Food Items Available]"
        """
        pos_str       = self.get_grid_position()
        food_type_str = self.get_food_type()
        items_count   = len(self.get_food_items())
        return f"Position {pos_str}: {food_type_str} Grid [{items_count} Food Items Available]"

    def __repr__(self):
        """
        Usually return something unambiguous, but per instructions,
        we can just return the same as __str__().
        """
        return self.__str__()
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

       
        if current_pos == top_right or current_pos == bottom_left:
            return sorted([top_left, bottom_right])

        
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
        # 부모 클래스(GameGrid) 생성자 호출
        super().__init__(grid_position, grid_dict, food_dict)

        # food_type을 "Special Food"로 덮어쓰기
        self.set_food_type("Special Food")

        # 특별 아이템 5개를 self.food_items로 설정
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
