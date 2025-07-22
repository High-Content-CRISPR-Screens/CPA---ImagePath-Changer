import pandas as pd
import sqlite3
 
def main():
    while True:
        db_path = input("Enter the path to the database file:")        
        if db_path == "":
            exit("No database path provided. Exiting.")
        db_path = db_path.replace('"','')
        if db_path.endswith('.db'):
            break

    
    conn = sqlite3.connect(db_path)
    
    cur = conn.cursor()

    df = pd.read_sql_query(f"SELECT name FROM sqlite_master WHERE type='table';", conn)
    experiment_name = df.loc[0, 'name'].replace("_Per_Object", "")

    columns_to_change = [ col for col in pd.read_sql_query(f"SELECT * FROM {experiment_name}_Per_Image LIMIT 0", conn).columns.tolist() if col.startswith("Image_PathName")]
    image_paths = pd.read_sql_query(f"SELECT {', '.join(columns_to_change)} FROM {experiment_name}_Per_Image", conn)
    unique_paths= pd.unique(image_paths.values.ravel())
    for path in unique_paths:
        new_path = input(f"Enter the new path for {path}:")
        for col in columns_to_change:
            cur.execute(f"UPDATE {experiment_name}_Per_Image SET {col} = ? WHERE {col} = ?", (new_path, path))
        conn.commit()

if __name__ == "__main__":
    main()