# Speech Recognition Models Comparison

This table provides a comparison of various speech recognition models on different parameters,based on test data with 20 samples.

| Model | Latency | WER | License | Free/Paid |
|-------|---------|-----|---------|-----------|
| seamlessm4t | 0.516299 | 0.319760 | Commercial | Paid |
| whisper | 1.219639 | 0.021075 | MIT License | Free |
| speechrecognition | 1.240599 | 0.021075 | BSD 3-Clause License | Free |
| deepgram | 2.234751 | 0.012821 | Proprietary | Paid |
| nemo | 10.439252 | 0.164815 | Apache 2.0 License | Free |
| speechmatics | 18.307120 | 0.040017 | Proprietary | Paid |

## Notes

- **Latency**: Measures the time (in seconds) taken by the model to process audio data.
- **WER (Word Error Rate)**: Indicates the accuracy of the model in transcribing speech, with lower values being better.
- **License**: Specifies the type of license under which the model is available.
 - **Commercial**: Indicates that the model is available for commercial use, typically with a paid license or subscription.
 - **MIT License**: A permissive open-source license that allows for commercial use, modification, distribution, and private use.
 - **BSD 3-Clause License**: Another permissive open-source license that allows for commercial use, modification, and distribution.
 - **Apache 2.0 License**: An open-source license that allows for commercial use, modification, and distribution, but with certain conditions for patent rights.
 - **Proprietary**: Indicates that the model is not open-source and is owned by a company, typically requiring a paid license or subscription for use.
- **Free/Paid**: Indicates whether the model is available for free or requires a paid subscription/license.

These results can be used to evaluate and compare the performance, accessibility, and licensing options of different speech recognition models based on your specific requirements and constraints.
