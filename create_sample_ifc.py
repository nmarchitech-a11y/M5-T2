import ifcopenshell, ifcopenshell.api, uuid

def create_residential_building():
    ifc = ifcopenshell.api.run("project.create_file", version="IFC4")
    project = ifcopenshell.api.run("root.create_entity", ifc, ifc_class="IfcProject", name="Residential House Project")
    ifcopenshell.api.run("unit.assign_unit", ifc)
    ctx = ifcopenshell.api.run("context.add_context", ifc, context_type="Model")
    body = ifcopenshell.api.run("context.add_context", ifc, context_type="Model", context_identifier="Body", target_view="MODEL_VIEW", parent=ctx)
    site = ifcopenshell.api.run("root.create_entity", ifc, ifc_class="IfcSite", name="Construction Site A")
    ifcopenshell.api.run("aggregate.assign_object", ifc, relating_object=project, products=[site])
    building = ifcopenshell.api.run("root.create_entity", ifc, ifc_class="IfcBuilding", name="Casa Residencial Modelo")
    ifcopenshell.api.run("aggregate.assign_object", ifc, relating_object=site, products=[building])
    gf = ifcopenshell.api.run("root.create_entity", ifc, ifc_class="IfcBuildingStorey", name="Ground Floor"); gf.Elevation = 0.0
    ff = ifcopenshell.api.run("root.create_entity", ifc, ifc_class="IfcBuildingStorey", name="First Floor"); ff.Elevation = 3.0
    ifcopenshell.api.run("aggregate.assign_object", ifc, relating_object=building, products=[gf, ff])
    
    mats = {}
    for n in ["Concrete C30","Clay Brick","Steel A36","Tempered Glass 6mm","Pine Wood","Ceramic Tile","Mineral Wool 50mm"]:
        mats[n] = ifcopenshell.api.run("material.add_material", ifc, name=n)

    def wall(name, storey, l, h, w, mat_name, ext=False, lb=False):
        e = ifcopenshell.api.run("root.create_entity", ifc, ifc_class="IfcWall", name=name)
        ifcopenshell.api.run("spatial.assign_container", ifc, relating_structure=storey, products=[e])
        ifcopenshell.api.run("material.assign_material", ifc, products=[e], material=mats[mat_name])
        ps = ifcopenshell.api.run("pset.add_pset", ifc, product=e, name="Pset_WallCommon")
        ifcopenshell.api.run("pset.edit_pset", ifc, pset=ps, properties={"IsExternal":ext,"LoadBearing":lb,"Width":w,"Reference":name})
        qs = ifcopenshell.api.run("pset.add_qto", ifc, product=e, name="Qto_WallBaseQuantities")
        ifcopenshell.api.run("pset.edit_qto", ifc, qto=qs, properties={"Length":l,"Height":h,"Width":w,"GrossSideArea":l*h,"GrossVolume":l*h*w,"NetVolume":l*h*w*0.85})
        return e

    def slab(name, storey, l, w, t, mat_name, ext=False):
        e = ifcopenshell.api.run("root.create_entity", ifc, ifc_class="IfcSlab", name=name)
        ifcopenshell.api.run("spatial.assign_container", ifc, relating_structure=storey, products=[e])
        ifcopenshell.api.run("material.assign_material", ifc, products=[e], material=mats[mat_name])
        ps = ifcopenshell.api.run("pset.add_pset", ifc, product=e, name="Pset_SlabCommon")
        ifcopenshell.api.run("pset.edit_pset", ifc, pset=ps, properties={"IsExternal":ext,"LoadBearing":True,"Reference":name})
        qs = ifcopenshell.api.run("pset.add_qto", ifc, product=e, name="Qto_SlabBaseQuantities")
        ifcopenshell.api.run("pset.edit_qto", ifc, qto=qs, properties={"Length":l,"Width":w,"Depth":t,"GrossArea":l*w,"GrossVolume":l*w*t})

    def door(name, storey, w, h, mat_name, ext=False):
        e = ifcopenshell.api.run("root.create_entity", ifc, ifc_class="IfcDoor", name=name); e.OverallWidth=w; e.OverallHeight=h
        ifcopenshell.api.run("spatial.assign_container", ifc, relating_structure=storey, products=[e])
        ifcopenshell.api.run("material.assign_material", ifc, products=[e], material=mats[mat_name])
        ps = ifcopenshell.api.run("pset.add_pset", ifc, product=e, name="Pset_DoorCommon")
        ifcopenshell.api.run("pset.edit_pset", ifc, pset=ps, properties={"IsExternal":ext,"Reference":name})

    def window(name, storey, w, h, mat_name):
        e = ifcopenshell.api.run("root.create_entity", ifc, ifc_class="IfcWindow", name=name); e.OverallWidth=w; e.OverallHeight=h
        ifcopenshell.api.run("spatial.assign_container", ifc, relating_structure=storey, products=[e])
        ifcopenshell.api.run("material.assign_material", ifc, products=[e], material=mats[mat_name])
        ps = ifcopenshell.api.run("pset.add_pset", ifc, product=e, name="Pset_WindowCommon")
        ifcopenshell.api.run("pset.edit_pset", ifc, pset=ps, properties={"IsExternal":True,"ThermalTransmittance":2.8,"GlazingAreaFraction":0.8,"Reference":name})

    def column(name, storey, h, mat_name):
        e = ifcopenshell.api.run("root.create_entity", ifc, ifc_class="IfcColumn", name=name)
        ifcopenshell.api.run("spatial.assign_container", ifc, relating_structure=storey, products=[e])
        ifcopenshell.api.run("material.assign_material", ifc, products=[e], material=mats[mat_name])
        qs = ifcopenshell.api.run("pset.add_qto", ifc, product=e, name="Qto_ColumnBaseQuantities")
        ifcopenshell.api.run("pset.edit_qto", ifc, qto=qs, properties={"Length":h,"CrossSectionArea":0.09,"GrossVolume":h*0.09})

    def beam(name, storey, l, mat_name):
        e = ifcopenshell.api.run("root.create_entity", ifc, ifc_class="IfcBeam", name=name)
        ifcopenshell.api.run("spatial.assign_container", ifc, relating_structure=storey, products=[e])
        ifcopenshell.api.run("material.assign_material", ifc, products=[e], material=mats[mat_name])
        qs = ifcopenshell.api.run("pset.add_qto", ifc, product=e, name="Qto_BeamBaseQuantities")
        ifcopenshell.api.run("pset.edit_qto", ifc, qto=qs, properties={"Length":l,"CrossSectionArea":0.06,"GrossVolume":l*0.06})

    # Ground Floor
    wall("GF-Ext-Wall-North",gf,10,3,0.25,"Clay Brick",True,True); wall("GF-Ext-Wall-South",gf,10,3,0.25,"Clay Brick",True,True)
    wall("GF-Ext-Wall-East",gf,8,3,0.25,"Clay Brick",True,True); wall("GF-Ext-Wall-West",gf,8,3,0.25,"Clay Brick",True,True)
    wall("GF-Int-Wall-Living-Kitchen",gf,5,3,0.15,"Clay Brick"); wall("GF-Int-Wall-Hall",gf,4,3,0.15,"Clay Brick"); wall("GF-Int-Wall-Bathroom",gf,2.5,3,0.15,"Clay Brick")
    slab("GF-Floor-Slab",gf,10,8,0.15,"Concrete C30")
    door("GF-Entrance-Door-Main",gf,1.0,2.1,"Pine Wood",True); door("GF-Entrance-Door-Back",gf,0.9,2.1,"Pine Wood",True)
    door("GF-Internal-Door-Kitchen",gf,0.8,2.1,"Pine Wood"); door("GF-Internal-Door-Bathroom",gf,0.7,2.1,"Pine Wood"); door("GF-Internal-Door-Hall",gf,0.8,2.1,"Pine Wood")
    window("GF-Window-Living-1",gf,1.5,1.2,"Tempered Glass 6mm"); window("GF-Window-Living-2",gf,1.5,1.2,"Tempered Glass 6mm")
    window("GF-Window-Kitchen-1",gf,1.2,1.0,"Tempered Glass 6mm"); window("GF-Window-Bathroom-1",gf,0.6,0.6,"Tempered Glass 6mm")
    for n in ["GF-Col-A1","GF-Col-A2","GF-Col-B1","GF-Col-B2","GF-Col-C1","GF-Col-C2"]: column(n,gf,3,"Concrete C30")
    beam("GF-Beam-North",gf,10,"Concrete C30"); beam("GF-Beam-South",gf,10,"Concrete C30"); beam("GF-Beam-East",gf,8,"Concrete C30"); beam("GF-Beam-West",gf,8,"Concrete C30"); beam("GF-Beam-Central",gf,10,"Concrete C30")
    
    # First Floor
    wall("1F-Ext-Wall-North",ff,10,3,0.25,"Clay Brick",True,True); wall("1F-Ext-Wall-South",ff,10,3,0.25,"Clay Brick",True,True)
    wall("1F-Ext-Wall-East",ff,8,3,0.25,"Clay Brick",True,True); wall("1F-Ext-Wall-West",ff,8,3,0.25,"Clay Brick",True,True)
    wall("1F-Int-Wall-Bedroom-Divider",ff,5,3,0.15,"Clay Brick"); wall("1F-Int-Wall-Hall-1F",ff,3,3,0.15,"Clay Brick")
    wall("1F-Int-Wall-Suite-Bath",ff,2,3,0.15,"Clay Brick"); wall("1F-Int-Wall-Closet",ff,2.5,3,0.15,"Clay Brick")
    slab("1F-Floor-Slab",ff,10,8,0.15,"Concrete C30"); slab("Roof-Slab",ff,10.5,8.5,0.12,"Concrete C30",True)
    door("1F-Door-Bedroom1",ff,0.8,2.1,"Pine Wood"); door("1F-Door-Bedroom2",ff,0.8,2.1,"Pine Wood")
    door("1F-Door-Bedroom3",ff,0.8,2.1,"Pine Wood"); door("1F-Door-Suite-Bath",ff,0.7,2.1,"Pine Wood")
    window("1F-Win-Bedroom1",ff,1.2,1.2,"Tempered Glass 6mm"); window("1F-Win-Bedroom2",ff,1.2,1.2,"Tempered Glass 6mm")
    window("1F-Win-Bedroom3",ff,1.5,1.2,"Tempered Glass 6mm"); window("1F-Win-Suite-Bath",ff,0.6,0.6,"Tempered Glass 6mm"); window("1F-Win-Hall",ff,1.0,1.0,"Tempered Glass 6mm")
    for n in ["1F-Col-A1","1F-Col-A2","1F-Col-B1","1F-Col-B2","1F-Col-C1","1F-Col-C2"]: column(n,ff,3,"Concrete C30")
    beam("1F-Beam-North",ff,10,"Concrete C30"); beam("1F-Beam-South",ff,10,"Concrete C30"); beam("1F-Beam-East",ff,8,"Concrete C30"); beam("1F-Beam-West",ff,8,"Concrete C30")

    # Stair + Railing
    st = ifcopenshell.api.run("root.create_entity", ifc, ifc_class="IfcStair", name="Main Staircase")
    ifcopenshell.api.run("spatial.assign_container", ifc, relating_structure=gf, products=[st])
    ifcopenshell.api.run("material.assign_material", ifc, products=[st], material=mats["Concrete C30"])
    ps = ifcopenshell.api.run("pset.add_pset", ifc, product=st, name="Pset_StairCommon")
    ifcopenshell.api.run("pset.edit_pset", ifc, pset=ps, properties={"NumberOfRiser":17,"NumberOfTreads":16,"RiserHeight":0.176,"TreadLength":0.28})
    rl = ifcopenshell.api.run("root.create_entity", ifc, ifc_class="IfcRailing", name="Stair Railing")
    ifcopenshell.api.run("spatial.assign_container", ifc, relating_structure=gf, products=[rl])
    ifcopenshell.api.run("material.assign_material", ifc, products=[rl], material=mats["Steel A36"])

    # Spaces
    rooms = [("Living Room",gf,25),("Kitchen",gf,15),("GF Bathroom",gf,5),("Entrance Hall",gf,8),("Laundry Room",gf,4),
             ("Master Bedroom",ff,20),("Bedroom 2",ff,14),("Bedroom 3",ff,12),("Suite Bathroom",ff,6),("1F Hall",ff,10),("Walk-in Closet",ff,5)]
    for rn, st, ar in rooms:
        sp = ifcopenshell.api.run("root.create_entity", ifc, ifc_class="IfcSpace", name=rn)
        ifcopenshell.api.run("aggregate.assign_object", ifc, relating_object=st, products=[sp])
        ps = ifcopenshell.api.run("pset.add_pset", ifc, product=sp, name="Pset_SpaceCommon")
        ifcopenshell.api.run("pset.edit_pset", ifc, pset=ps, properties={"IsExternal":False,"GrossFloorArea":ar,"NetFloorArea":ar*0.92,"Reference":rn})
        qs = ifcopenshell.api.run("pset.add_qto", ifc, product=sp, name="Qto_SpaceBaseQuantities")
        ifcopenshell.api.run("pset.edit_qto", ifc, qto=qs, properties={"GrossFloorArea":ar,"NetFloorArea":ar*0.92,"Height":3.0,"GrossVolume":ar*3.0})

    out = "/home/claude/ifc-analyzer-project/casa_residencial.ifc"
    ifc.write(out)
    v = ifcopenshell.open(out)
    for t in ["IfcWall","IfcDoor","IfcWindow","IfcSlab","IfcColumn","IfcBeam","IfcStair","IfcSpace","IfcRailing"]:
        c = len(v.by_type(t)); 
        if c: print(f"  {t}: {c}")
    print(f"✅ IFC saved: {out}")

if __name__=="__main__": create_residential_building()
