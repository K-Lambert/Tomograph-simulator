"""
This program using images imported from dicom files, calculate sinogram using mathematical 
formulas and then recreate image from sinogram. Program calculate detectors and emitter 
position during rotation. New image can be filtered or not. It also show image recreating 
process by saving and showing every tenth tomograph step.
"""


from radon_transform import *
from rmse import *
from save_to_dicom import *

import matplotlib.pyplot as plt


def main():
    print("PROGRAM START")


    # READ FILE
    try:
        filename = "tomograph-dicom\shepp_logan.dcm"
        ds = pydicom.dcmread(filename)
    except:
        print("[ERROR:] Cannot read file")
        return
    

    # STREAMLIT - SINOGRAM VARIABLES SETTINGS   
    st.title("Tomograph simulator")
    steps_number = st.slider("Number of steps",90,720,180,90)           # Number of steps
    alpha = 360/steps_number    
    print(f"Alpha: {alpha}")                                            # Step a emmiter/detector.
    detector_number = st.slider("Number of detectors",90,720,180,90)    # Quantity of detectors
    detector_angle = st.slider("Detector angle",45,270,180,45)          # Angle between detectors

    # STREAMLIT - PATIENT DATA 
    patient_data_form = st.form("patient_data_form")
    patient_data_form.title("Save to file")
    name = patient_data_form.text_input("First name")
    surname = patient_data_form.text_input("Last name")
    date = patient_data_form.date_input("Diagnosis date")
    comment = patient_data_form.text_input("Comment")
    filename = patient_data_form.text_input("Filename")
    patient_data_form_submitted = patient_data_form.form_submit_button("Change Values")
    

    # Images
    orginal_image = ds.pixel_array
    sinogram = radon_transform(orginal_image, steps_number, alpha, detector_number,detector_angle)
    
    # If checkbox checked filter recreated image
    filtered = st.checkbox("Filter")

    # Recreating image from sinogram
    kernel = []
    for k in range(-10,11):
        if k == 0:
            kernel.append(1)
        elif k % 2 == 0:
            kernel.append(0)
        else:
            kernel.append((-4/(math.pi ** 2)) / (k ** 2))

    new_array = []
    for i in range(len(sinogram)):
        new_array.append(np.convolve(sinogram[i], kernel, mode='same'))

    if filtered:
        reverse_image, partial_reverse_images = reverse_radon_transform(orginal_image, steps_number, alpha, detector_number, detector_angle, new_array, True)
        reverse_image = rescale_intensity(reverse_image, in_range=(0, 255), out_range=(0, 255))
    else:
        reverse_image, partial_reverse_images = reverse_radon_transform(orginal_image, steps_number, alpha, detector_number, detector_angle, sinogram)

    number_of_image = st.slider("Image number",0,(len(partial_reverse_images)-1),1,1)
    current_image =  partial_reverse_images[number_of_image]

    rmse = count_rmse(orginal_image, current_image)
    st.write(f"RMSE: {round(rmse, 4)} ")


    # PLOT
    fig1, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 10))
    fig2, (ax4) = plt.subplots(1, 1, figsize=(8, 10))
    
    # Subplot 1
    ax1.set_title("Orginal")
    ax1.imshow(orginal_image, cmap=plt.cm.Greys_r)
    
    # Subplot 2
    ax2.set_title("Sinogram")
    if filtered:
        ax2.imshow(new_array, cmap=plt.cm.Greys_r)
    else:
        ax2.imshow(sinogram, cmap=plt.cm.Greys_r)

    # Subplot 3
    ax3.set_title("Reverse Radon transform")
    ax3.imshow(reverse_image, cmap=plt.cm.Greys_r)
    st.pyplot(fig1)

    # Subplot 4
    ax4.imshow(current_image, cmap=plt.cm.Greys_r)
    st.pyplot(fig2) 

    print("CALCULATIONS END")


    try:
        st.write(ds.ContentDate)
    except:
        st.write("No date")
    try:
        st.write(ds.ImageComments)
    except:
        st.write("No comments")

    if patient_data_form_submitted:
        patient_info_dict = {}
        # DICOM INFORMATIONS

        patient_info_dict["PatientName"] = name+" "+surname
        patient_info_dict["Date"] = date.strftime("%Y%m%d")
        patient_info_dict["ImageComments"] = comment

        if not filename:
            filename = "default"
        save_as_dicom(f"tomograph_saved_dicom_files/{filename}.dcm", reverse_image, patient_info_dict)
        st.write("Data saved")
        st.write(patient_info_dict["PatientName"])
        st.write(patient_info_dict["Date"])
        st.write(patient_info_dict["ImageComments"])


        print("PROGRAM END")

if __name__ == "__main__":
    main()