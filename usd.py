import omni.usd
from pxr import UsdGeom, Usd, Gf, Kind

BOX_WIDTH = 53.0
BOX_HEIGHT = 53.0

boxes = {
    "Cardbox_B2": "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/ArchVis/Industrial/Containers/Cardboard/Cardbox_B2.usd",
    "Cardbox_B3": "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/ArchVis/Industrial/Containers/Cardboard/Cardbox_B3.usd"
}

def add_palette(stage, parent_prim):
    xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, parent_prim.GetPath().AppendPath("Pallet_A1"))
    prim: Usd.Prim = xform.GetPrim()
    prim.GetReferences().AddReference("http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/ArchVis/Industrial/Pallets/Pallet_A1.usd")
    xform.AddTranslateOp(UsdGeom.XformOp.PrecisionDouble)
    xform.AddRotateXYZOp(UsdGeom.XformOp.PrecisionDouble).Set(Gf.Vec3d([-90, 0, 0]))
    xform.AddScaleOp(UsdGeom.XformOp.PrecisionDouble)
    
def add_boxes(stage, parent_prim, y_pos: float=21, y_rot: float= 0):
    start_x = -(BOX_WIDTH / 2)
    for i, box_name in enumerate(boxes):
        xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, parent_prim.GetPath().AppendPath(box_name))
        prim: Usd.Prim = xform.GetPrim()
        prim.GetReferences().AddReference(boxes[box_name])
        xform.AddTranslateOp(UsdGeom.XformOp.PrecisionDouble).Set(Gf.Vec3d([start_x + i * BOX_WIDTH, y_pos, 0]))
        xform.AddRotateXYZOp(UsdGeom.XformOp.PrecisionDouble).Set(Gf.Vec3d([-90, y_rot, 0]))
        xform.AddScaleOp(UsdGeom.XformOp.PrecisionDouble)
    
def add_boxes1(stage, parent_prim, y_pos: float=21, y_rot: float= 0):
    start_x = 0
    for i, box_name in enumerate(boxes):
        xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, parent_prim.GetPath().AppendPath(box_name))
        prim: Usd.Prim = xform.GetPrim()
        prim.GetReferences().AddReference(boxes[box_name])
        xform.AddTranslateOp(UsdGeom.XformOp.PrecisionDouble).Set(Gf.Vec3d([start_x, y_pos + i * BOX_HEIGHT, 0]))
        xform.AddRotateXYZOp(UsdGeom.XformOp.PrecisionDouble).Set(Gf.Vec3d([-90, y_rot, 0]))
        xform.AddScaleOp(UsdGeom.XformOp.PrecisionDouble)
    
stage: Usd.Stage = omni.usd.get_context().get_stage()
# Need to remove the default prim to fully remove variant spec
stage.RemovePrim("/World")
default_prim = UsdGeom.Xform.Define(stage, "/World").GetPrim()
stage.SetDefaultPrim(default_prim)

config: Usd.VariantSet = default_prim.GetVariantSets().AddVariantSet("configuration")
config.AddVariant("default")
config.AddVariant("rotated")
config.AddVariant("stackedOnTop")
config.SetVariantSelection("default")

# Create the empty palette outside of the Variant Set
add_palette(stage, default_prim)

# Create the default config with boxes
with config.GetVariantEditContext():
    add_boxes(stage, default_prim)

# Create an alternate config with the boxes for variation
config.SetVariantSelection("rotated")
with config.GetVariantEditContext():
    add_boxes(stage, default_prim, y_rot=90)
    
config.SetVariantSelection("stackedOnTop")
with config.GetVariantEditContext():
    add_boxes1(stage, default_prim)

config.SetVariantSelection("default")

Usd.ModelAPI(default_prim).SetKind(Kind.Tokens.assembly) # Should this be added as a separate step? Maybe we could elaborate more on it
