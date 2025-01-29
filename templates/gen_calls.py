

if __name__ == "__main__":
    hours = [1.5, 2.5, 3.5]
    times = [15, 33, 60, 90]
    areas = [50, 100, 200, 400]

    sl = 365.25*3

    with open("templates.sh", "w") as f:
        f.write("python baseline.py --survey_length %.2f \n" % sl)
        for h in hours:
            for t in times:
                for a in areas:
                    f.write("python templates.py --survey_length %.2f --template_ha_range %.2f --template_time %.2f --template_area %.2f \n" % (sl, h, t, a))
