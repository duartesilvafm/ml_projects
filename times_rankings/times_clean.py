
import pandas as pd

def times_clean(x, data, year = None):
    
    # assert x is an int   
    assert type(x) == int, "Your top value is not in a valid format, please enter an integer"
    assert type(data) == pd.core.frame.DataFrame, "Data has to be in a pandas dataframe format"
    
    # make total_score numeric
    data["total_score"] = pd.to_numeric(data["total_score"], errors = "coerce")
    
    # drop NAs in total_score
    data.dropna(subset = ["total_score"], inplace = True)
    
    # make sure values in the total_score column are sorted
    data.sort_values(by = "total_score", ascending = False)
    
    # filter by only the selected year
    if year != None:
        data = data[data["year"] == year]
        
    # Convert all other columns to float type
    data["international"] = pd.to_numeric(data["international"], errors = "coerce")
    data["income"] = pd.to_numeric(data["income"], errors = "coerce") 
    data["female_male_ratio"] = pd.to_numeric(data["female_male_ratio"].apply(lambda d: str(d).split(" : ")[0]), errors = "coerce")
    data["international_students"] = pd.to_numeric(data["international_students"].apply(lambda d: str(d).split("%")[0]), errors = "coerce")
    data["num_students"] = pd.to_numeric(data["num_students"].apply(lambda d: str(d).replace(",", ".")), errors = "coerce")
    
    # find the nth_score
    scores = list(data["total_score"])
    score_x = scores[x]
    
    # code output variable
    data["top_" + str(x)] = data["total_score"].apply(lambda d: 1 if d >= score_x else 0) 
    
    return data
