def constraint_max_min(xmin,ymin,xmax,ymax,width,height):

    if xmin<0:
        xmin=0
    if ymin<0:
        ymin=0
    if xmax>width:
        xmax=width
    if ymax>height:
        ymax=height

    return xmin,ymin,xmax,ymax

def func_filter_img(xyxy,label,constraint,img0):

    xmin,ymin,xmax,ymax = int(xyxy[0].cpu().numpy()),int(xyxy[1].cpu().numpy()),int(xyxy[2].cpu().numpy()),int(xyxy[3].cpu().numpy())
    w,h = constraint.get(label)
    if (xmax-xmin)<w or (ymax-ymin)<h:
        return True
    if xmin==0 or xmax==img0.shape[0]:# edge
        return True
    return False