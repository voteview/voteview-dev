import vvtool.app


vvtool.app.connect("voteviewtest")

vvtool.app.Person.objects(bioguide_id="A000001").update(
    set__biography="A new biography."
)
