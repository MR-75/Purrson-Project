
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

