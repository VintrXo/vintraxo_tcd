open("sales.csv", "w", encoding="utf-8").write("""date,branch,product,category,qty,price
2025-01-05,Riyadh,Laptop,Electronics,2,3500
2025-01-07,Jeddah,Smartphone,Electronics,3,2200
2025-01-09,Riyadh,Notebook,Stationery,40,15
2025-01-12,Dammam,Office chair,Furniture,4,600
2025-01-15,Jeddah,Headphones,Electronics,,250
2025-01-18,Riyadh,Colored pens,Stationery,25,25
2025-01-21,Dammam,Wooden desk,Furniture,1,1200
2025-01-24,Jeddah,Backpack,Accessories,6,180
2025-02-02,Riyadh,Smartphone,Electronics,5,2200
2025-02-04,Dammam,Notebook,Stationery,60,15
2025-02-08,Jeddah,Laptop,Electronics,1,3500
2025-02-11,Riyadh,Office chair,Furniture,3,600
2025-02-14,,Headphones,Electronics,7,250
2025-02-17,Jeddah,Colored pens,Stationery,30,25
2025-02-20,Dammam,Backpack,Accessories,4,180
2025-02-20,Dammam,Backpack,Accessories,4,180
2025-03-03,Riyadh,Wooden desk,Furniture,2,1200
2025-03-06,Jeddah,Smartphone,Electronics,4,2200
2025-03-10,Dammam,Laptop,Electronics,2,3500
2025-03-14,Riyadh,Headphones,Electronics,10,250
""")
open("branches.csv", "w", encoding="utf-8").write("""branch,manager,opened
Riyadh,Sara Ahmed,2019
Jeddah,Omar Khaled,2021
Dammam,Layla Hassan,2023
""")
