

if __name__ == "__main__":
    hours = [1.5, 2.5, 3.5]
    times = [15, 33, 60, 90]
    areas = [50, 100, 200, 400]

    with open("templates.sh", "w") as f:
        for h in hours:
            for t in times:
                for a in areas:
                    f.write("python templates.py --template_ha_range %.2f --template_time %.2f --template_area %.2f \n" % (h, t, a))
