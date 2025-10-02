## Step1
Please first check if you have Cisco installed, you need it to connect to school internet so you can login the labeling working space. The host machine is a laptop in IGB. If not, you can download it here:

*https://webstore.illinois.edu/Shop/product.aspx?zpid=2600*

Follow the tutorial here to download label studio, the most popular labeling tool.

Perhaps the easiest way is to install via pip. You will be required to create an account, feel free to use any emails, this account will only be used in this local internet. 

*https://github.com/HumanSignal/label-studio?tab=readme-ov-file#install-locally-with-pip*

You need to activate tour VPN before proceeding to next step.

## Step2
There is a link to our own working space, it is not permanent, so if you need it, either come to IGB to create one from host machine or contact us.

Click the link, then it will go to our working space directly.

## Step3 Image Collection
There are some tips for collecting images.

1. Make the background varied, but it’s preferable if it resembles a laboratory or biohood environment.
2. Multiple objects can appear in a single image.
3. Pay attention to keeping the occurrence of different object types relatively balanced; otherwise, it may affect the final training results, so this should be controlled during shooting.
4. Different lighting conditions may be included, as well as reflections.
5. Try to avoid having a large number of objects concentrated in the corners of the image, as this will make annotation more difficult.

These pictures will be regarded as raw images. Once these images are collected, they should be uploaded to host machine and everyone in the shared working space and see them and label them.

## Step4 Labeling
There are some requirements for labeling.

1. Only use upright rectangular boxes to select objects. Do not draw contours or filled shapes (those are for image segmentation), and do not use tilted boxes — the edges must be strictly horizontal or vertical.

2. If the object’s outline is clear, try to draw the bounding box as precisely as possible.

3. Every object in the image needs to be boxed. The principle is: if the annotator can recognize it, it should be annotated.

4. If an object is partially occluded, only box the visible part. Do not imagine or reconstruct its original full shape or size.

Once this step is finished, please let another person do cross-validation.

## Step5 Augmentation
Details about this step will be added later.

## PS
### To move image directory
**Step 1**

If the address of image must be changed, you should first go to the project, export a JSON (not JSON MIN). Then use function *update_json_paths* in *yolo_utils.py* to modify the address of all images. Then this file contains all correct annotation information.

**Step 2**

Create a new project, use *cloud storage*, and then select *local files* as storage surce. The source address should be the new address of images. But do not syncronize!!

**Step 3**

Then input the following code as labeling interface:
```python
<View>
  <Header value="Select a tool and annotate the image"/>
  <Image name="image" value="$image" rotateControl="false" zoom="true"/>

  <!-- Rectangle -->
  <RectangleLabels name="rect" toName="image" strokeWidth="2">
    <Label value="Pipette"             background="#FFA39E"/>
    <Label value="Petri dish"          background="#FFC069"/>
    <Label value="Pipette tip holder"  background="#AD8B00"/>
    <Label value="Tube holder"         background="#D3F261"/>
    <Label value="Suction tip"         background="#389E0D"/>
    <Label value="Beaker"              background="#5CDBD3"/>
    <Label value="MEA"                 background="#096DD9"/>
    <Label value="Large centri-tube"   background="#ADC6FF"/>
    <Label value="Middle centri-tube"  background="#9254DE"/>
    <Label value="Mini centri-tube"    background="#F759AB"/>
    <Label value="rectangle bottle"    background="#D4380D"/>
  </RectangleLabels>

</View>
```

Then improt the modified JSON file, and you will find all figures reappear in the new project.
