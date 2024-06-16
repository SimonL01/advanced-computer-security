import pandas as pd

# Discrete Logarithm
# dlog_b(x) = y such that b^y mod p = x, where 

# prime p such that p > 2
# g in Z*_p where Z_p is the set of all integers that are congruent modulo p in the set {0, 1, 2, ..., p-1}
# consider the function f(x) = g^x in Z_p
# now consider the inverse function dlog_g(g^x) = x, x in {0, 1, 2, ..., p-2} 

def compute_discrete_log(g,p):
    results = {}
    current_value = 1
    for x in range(p-1):
        # print x
        #print(f"x : {x}, current_value : {current_value}")
        results[current_value] = x
        current_value = (current_value*g) % p
    # print(results)
    return results

# Generator and prime number
g = 2
p = 11

# Compute the discrete logarithm table
discrete_log_table = compute_discrete_log(g,p)

# Create a DataFrame for the results
df = pd.DataFrame(list(discrete_log_table.items()), columns=["g^x", "dlog_g(g^x)"])

# print(f"Discrete Log Table : {discrete_log_table}")

# print each discrete_log_table[x]
# for x in discrete_log_table:
    # print(f"x : {x}, discrete_log_table[x] : {discrete_log_table[x]}")
    # x is g^x
    # discrete_log_table[x] is dlog_g(g^x) = x

# Sort the DataFrame by the 'g^x mod p' column
df = df.sort_values(by='g^x').reset_index(drop=True)

# Compute the '2^dlog_g(g^x) mod 11' column
df['2^dlog_g(g^x) mod 11'] = df['dlog_g(g^x)'].apply(lambda x: (g**x) % p)

# Display the DataFrame
print(df)