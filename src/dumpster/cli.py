from cyclopts import App


app = App(name="dumpster", help="Keep track of local database state without worry.")


@app.default
def main():
    print("Okay okay")


if __name__ == "__main__":
    app()
