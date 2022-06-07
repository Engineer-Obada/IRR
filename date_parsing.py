import re
def ourDate(contentAFile):
    dates = re.findall("(0[1-9]|[12]\d|3[01])[/.-]"
                       "(0[1-9]|1[012])"
                       "[/.-](\d{4})", contentAFile)
    dates.extend(re.findall("(0[1-9]|[12]\d|3[01])[/.-]"
                            "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
                            "[/.-](\d{4})", contentAFile))
    dates.extend(re.findall("(0[1-9]|[12]\d|3[01])[/.-]"
                            "(January|February|March|April|May|June|July|August|September|October|November|December)"
                            "[/.-](\d{4})", contentAFile))
    return dates


def convert_to_regular_date(s):
    # s is output ==>   re.findall("regEx",str)
    _date = []
    s1 = ""
    for d in s:
        s1 = d[0]
        s1 += "-"
        if d[1] == "01" or d[1] == "January":
            s1 += "Jan"
        elif d[1] == "02" or d[1] == "February":
            s1 += "Feb"
        elif d[1] == "03" or d[1] == "March":
            s1 += "Mar"
        elif d[1] == "04" or d[1] == "April":
            s1 += "Apr"
        elif d[1] == "05" or d[1] == "May":
            s1 += "May"
        elif d[1] == "06" or d[1] == "June":
            s1 += "Jun"
        elif d[1] == "07" or d[1] == "July":
            s1 += "Jul"
        elif d[1] == "08" or d[1] == "August":
            s1 += "Aug"
        elif d[1] == "09" or d[1] == "September":
            s1 += "Sep"
        elif d[1] == "10" or d[1] == "October":
            s1 += "Oct"
        elif d[1] == "11" or d[1] == "November":
            s1 += "Nov"
        elif d[1] == "12" or d[1] == "December":
            s1 += "Dec"
        else:
            s1 += d[1]

        s1 += "-{}".format(d[2])
        _date.append(s1)
    return _date
