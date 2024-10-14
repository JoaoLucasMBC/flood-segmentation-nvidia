import onnxruntime as ort
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

class FloodModel:

    def __init__(self, model_path, verbose=False):
        self.model = ort.InferenceSession(model_path)
        self.input_name = self.model.get_inputs()[0].name
        self.output_name = self.model.get_outputs()[0].name
        self.verbose = verbose

        if self.verbose:
            print(f"Session initialized: {self.model}")

    def predict(self, image_path, output_path):
        image = Image.open(image_path).convert('RGB')
        image = self.preprocess_image(image)
        result = self.model.run([self.output_name], {self.input_name: image})

        if self.verbose:
            print("Shape of the result: ", result[0].shape)
    
        # Remove batch and channel dimensions (squeeze to get shape (512, 512))
        mask = np.squeeze(result[0], axis=(0, 3))  # Removes batch and channel dimensions

        # Convert mask to an image and save it
        mask_img = Image.fromarray(np.uint8(mask * 255))  # Scale values if necessary

        mask_img.save(output_path)

        self.image_path = image_path
        self.output_path = output_path

        return result
    
    
    def preprocess_image(self, image): 
        """
        This function returns the pre-processed image as a NumPy array. 
        """
        # Take away the A from RGBA
        image = image.convert('RGB')

        # load image as a 32-bit floating point array 
        image_ary=np.asarray(image)
        image_ary=image_ary.astype(np.float32)
            
        # pre-processing
        image_ary=(image_ary-127.5)*(1/127.5)
        
        # the sample_resnet18 segmentation model requires the data to be in BGR format
        BGR=np.empty_like(image_ary)
        BGR[:, :, 0]=image_ary[:, :, 2]
        BGR[:, :, 1]=image_ary[:, :, 1]
        BGR[:, :, 2]=image_ary[:, :, 0]
        image_ary=BGR
        
        # convert array from h, w, c to 1, c, h, w
        image_ary=np.transpose(image_ary, [2, 0, 1])
        image_ary=np.expand_dims(image_ary, axis=0)

        if self.verbose:
            print("Image array shape: ", image_ary.shape)

        return image_ary
    
    def plot(self):
        # plot input, triton inference, and ground truth
        fig, ax=plt.subplots(1, 2, figsize=[20, 5], sharex=True, sharey=True)
        ax[0].imshow(plt.imread(self.image_path))
        ax[1].imshow(plt.imread(self.output_path))

        # set title
        ax[0].set_title('Input Image')
        ax[1].set_title('Inference')

        # remove ticks
        ax[0].set_xticks([])
        ax[0].set_yticks([])



if __name__ == "__main__":
    import os

    model_path = os.listdir("./model")[0]
    model = FloodModel(os.path.join("./model", model_path), verbose=True)

    for filename in os.listdir("./input"):
        model.predict(os.path.join("./input", filename), os.path.join("./output", filename))

    print("Prediction finished!")