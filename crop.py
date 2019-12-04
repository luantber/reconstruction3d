import cv2
import numpy as np
runsingleimage=None
import sys
import show3d

def mouseCallback(tp,mousey,mousex,*args):
        global xy0,xy1,cur_drag,start_drag_xy
        if tp==0:
            if cur_drag==0:
                dy=mousey-xy1[1]
                nx=int(dy*3/4)+xy1[0]
                xy0=(nx,mousey)
            elif cur_drag==1:
                dy=mousey-xy0[1]
                nx=int(dy*3/4)+xy0[0]
                xy1=(nx,mousey)
            elif cur_drag==2:
                nx=xy0[0]+mousex-start_drag_xy[0]
                ny=xy0[1]+mousey-start_drag_xy[1]
                xy0=(nx,ny)
                nx=xy1[0]+mousex-start_drag_xy[0]
                ny=xy1[1]+mousey-start_drag_xy[1]
                xy1=(nx,ny)
                start_drag_xy=(mousex,mousey)
        elif tp==1:
            dist1=(xy0[0]-mousex)**2+(xy0[1]-mousey)**2
            dist2=(xy1[0]-mousex)**2+(xy1[1]-mousey)**2
            if min(dist1,dist2)>100:
                if mousex>=xy0[0] and mousex<=xy1[0] and mousey>=xy0[1] and mousey<=xy1[1]:
                    start_drag_xy=(mousex,mousey)
                    cur_drag=2
            else:
                if dist1<dist2:
                    cur_drag=0
                else:
                    cur_drag=1
        elif tp==4:
            cur_drag=-1

def run(imagen,imagen_mask,filename="default"):
    global xy0,xy1,cur_drag,start_drag_xy
    overlay=np.zeros((192,256,3),dtype='uint8')
    h,w=overlay.shape[:2]
    focus=400
    cx,cy=overlay.shape[0]/2,overlay.shape[1]/2
    beta=20.0/180.0*np.pi


    viewmat=np.array([[
        np.cos(beta),0,-np.sin(beta)],[
        0,1,0],[
        np.sin(beta),0,np.cos(beta)]],dtype='float32')


    for t in np.linspace(0,2*np.pi,1000):
        xyz=np.array([0,np.cos(t)/1.8,np.sin(t)/1.8])
        xyz=viewmat.T.dot(xyz)+[0.14,0,-2]
        x=int(cx+xyz[0]/-xyz[2]*focus)
        y=int(cy+xyz[1]/-xyz[2]*focus)
        
        cv2.circle(overlay,(y,x),1,(0,0,255))

        xyz=np.array([-np.sin(t/2)/1.8,np.cos(t/2)/1.8,0])
        xyz=viewmat.T.dot(xyz)+[0.14,0,-2]
        x=int(cx+xyz[0]/-xyz[2]*focus)
        y=int(cy+xyz[1]/-xyz[2]*focus)
        cv2.circle(overlay,(y,x),1,(0,0,255))

        for k in [-1,-0.5,0,0.5,1]:
            xyz=np.array([0,(t-np.pi)/np.pi/1.8,k/1.8])
            xyz=viewmat.T.dot(xyz)+[0.14,0,-2]
            x=int(cx+xyz[0]/-xyz[2]*focus)
            y=int(cy+xyz[1]/-xyz[2]*focus)
            cv2.circle(overlay,(y,x),0,(255,0,0))

        for k in [-1,-0.5,0,0.5,1]:
            xyz=np.array([0,k/1.8,(t-np.pi)/np.pi/1.8])
            xyz=viewmat.T.dot(xyz)+[0.14,0,-2]
            x=int(cx+xyz[0]/-xyz[2]*focus)
            y=int(cy+xyz[1]/-xyz[2]*focus)
            cv2.circle(overlay,(y,x),0,(255,0,0))

        xyz=np.array([-0.5/1.8,1/1.8,(t-np.pi)/np.pi/1.8])
        xyz=viewmat.T.dot(xyz)+[0.14,0,-2]
        x=int(cx+xyz[0]/-xyz[2]*focus)
        y=int(cy+xyz[1]/-xyz[2]*focus)
        cv2.circle(overlay,(y,x),0,(0,255,0))

        xyz=np.array([-0.5/1.8,-1/1.8,(t-np.pi)/np.pi/1.8])
        xyz=viewmat.T.dot(xyz)+[0.14,0,-2]
        x=int(cx+xyz[0]/-xyz[2]*focus)
        y=int(cy+xyz[1]/-xyz[2]*focus)
        cv2.circle(overlay,(y,x),0,(0,255,0))

        xyz=np.array([-0.5/1.8,(t-np.pi)/np.pi/1.8,1/1.8])
        xyz=viewmat.T.dot(xyz)+[0.14,0,-2]
        x=int(cx+xyz[0]/-xyz[2]*focus)
        y=int(cy+xyz[1]/-xyz[2]*focus)
        cv2.circle(overlay,(y,x),0,(0,255,0))

        xyz=np.array([-0.5/1.8,(t-np.pi)/np.pi/1.8,-1/1.8])
        xyz=viewmat.T.dot(xyz)+[0.14,0,-2]
        x=int(cx+xyz[0]/-xyz[2]*focus)
        y=int(cy+xyz[1]/-xyz[2]*focus)
        cv2.circle(overlay,(y,x),0,(0,255,0))
    overlay_mask=overlay.sum(axis=-1,keepdims=True)!=0

    img_in=imagen
    img_mask=imagen_mask
    # modelname=sys.argv[3]
    assert img_in.shape[:2]==img_mask.shape[:2]
    h,w=img_in.shape[:2]
    h2,w2=384,512
    if h*w2>h2*w:
        h2=h2
        w2=w*h2/h
    else:
        w2=w2
        h2=h*w2/w
    h,w=int(h2),int(w2)
    img_in=cv2.resize(img_in,(w,h))
    img_mask=cv2.resize(img_mask,(w,h))

    xy0=int(h/8),int(w/8)
    xy1=int(h-h/8),int(w-w/8)

    mousexy=[(0,0)]
    cur_drag=-1
    start_drag_xy=(0,0)
    
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',mouseCallback)

    xyzs=None
    while True:
        show=img_in.copy()
        cv2.rectangle(show,(xy0[1],xy0[0]),(xy1[1],xy1[0]),(0,0,255))
        for x,y in [xy0,xy1]:
            cv2.circle(show,(y,x),5,(0,0,255),-1)
            cv2.circle(show,(y,x),4,(255,255,255),-1)
        x0,y0=xy0
        x1,y1=xy1
        cropped=cv2.warpAffine(img_in,cv2.getAffineTransform(np.array(
            [[y0,x0],[y0,x1],[y1,x1]],dtype='float32'),np.array(
            [[-0.5,-0.5],[-0.5,overlay.shape[0]-0.5],[overlay.shape[1]-0.5,overlay.shape[0]-0.5]],dtype='float32')),
            (overlay.shape[1],overlay.shape[0])
        )
        cropped_mask=cv2.warpAffine(img_mask,cv2.getAffineTransform(np.array(
            [[y0,x0],[y0,x1],[y1,x1]],dtype='float32'),np.array(
            [[-0.5,-0.5],[-0.5,overlay.shape[0]-0.5],[overlay.shape[1]-0.5,overlay.shape[0]-0.5]],dtype='float32')),
            (overlay.shape[1],overlay.shape[0])
            )[:,:,0]>0.

        # print ((cropped-(cropped/2*cropped_mask[:,:,None])).dtype	) 
        # print ( (overlay*(overlay_mask)).dtype ) 
        show_cropped= np.array((cropped-(cropped/2*cropped_mask[:,:,None]))*(~overlay_mask),dtype=np.uint8)|(overlay*(overlay_mask))
        cv2.imshow('image',show)
        cv2.imshow('cropped',show_cropped)
        if xyzs is not None:
            cmd=show3d.showpoints(xyzs,waittime=10)%256
        else:
            cmd=cv2.waitKey(10)%256
        if cmd==ord('q'):
            break
        elif cmd==ord('l'):
            rects=np.loadtxt(filename+'.rect.txt')
            x0=int(np.round(rects[0,0]))
            y0=int(np.round(rects[0,1]))
            x1=int(np.round(rects[1,0]))
            y1=int(np.round(rects[1,1]))
            xy0=(x0,y0)
            xy1=(x1,y1)
        elif cmd==ord(' '):
            np.savetxt(filename+'.rect.txt',[[x0,y0],[x1,y1]])
            return cropped , np.uint8(cropped_mask)*255
            
            # if runsingleimage is None:
            #     import runsingleimage
            #     model=runsingleimage.loadModel(modelname)
            # # cv2.imwrite('%s.crop.png'%sys.argv[1],cropped)
            # # cv2.imwrite('%s.crop_m.png'%sys.argv[1],np.uint8(cropped_mask)*255)
            # xyzs=runsingleimage.run_image(model,cropped,cropped_mask)
            # np.savetxt('%s.xyz'%sys.argv[1],xyzs)
