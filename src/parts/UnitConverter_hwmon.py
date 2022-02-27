#CONVERTS FROM BITS TO EXABYTES BOTH WAYS
def divide(place, limit, x, by):
    if place >= limit:
        return x
    else:
        res = x / by
        if place == 0 or place == 1:
            by = 8
        return divide(place + 1, limit, res, by)


def mult(place, limit, x, by):
    if place <= limit:
        return x
    else:
        res = x * by
        # print(f"RES::: {res}\nPLACE::: {place}")
        if place == 0 or place == 1:
            by = 8
        return mult(place - 1, limit, res, by)


def convert(amt, frm, to):
    tableAbbrv = ["bit", "byte", "Kb", "Mb", "Gb", "Tb", "Eb"]
    conversionTable = {"bit": 0, "byte": 1, "kilobyte": 2, "megabyte": 3, "gigabyte": 4, "terrabyte": 5, "exabyte": 6}
    frmLvl = conversionTable[frm]
    toLvl = conversionTable[to]
    steps = toLvl - frmLvl
    newUnit = tableAbbrv[toLvl]
    # print(f"GO {steps} STEPS")
    # print("CONVERT {0} {1} TO {2}".format(amt, frm, newUnit))
    # print(f"FROMLVL::: {frmLvl}\ntoLvl::: {toLvl}")
    # print("GOT: {}".format(res))
    #if steps < 0 we are going down
    if steps < 0:
        res = mult(frmLvl, toLvl, amt, 1000)
    elif steps > 0:
        res = divide(frmLvl, toLvl, amt, 1000)
    else:
        # print("YOU ARE TRYING TO CONVERT THE SAME VALUE!")
        return amt, tableAbbrv[frmLvl]
    # print(res)
    
    return res, newUnit



if __name__ == "__main__":
    # myResult = convert(4096, "gigabyte", "kilobyte")
    # print (f"4096 GB to {myResult}")
    myResult, unit = convert(4096, "kilobyte", "byte")
    print(f"CHECKING DIVIDE: 4096 kb to {myResult}")
