import vvcli.app


vvcli.app.connect("voteviewtest")

vvcli.app.Person.objects(bioguide_id="A000001").update(
    set__biography="A new biography."
)
