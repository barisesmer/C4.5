
1. Title of Database: Optical Recognition of Handwritten Digits
		Original, unnormalized version.

2. Source:
	E. Alpaydin, C. Kaynak
	Department of Computer Engineering
	Bogazici University, 80815 Istanbul Turkey
	alpaydin@boun.edu.tr
	September 1998

3. Past Usage:
	C. Kaynak (1995) Methods of Combining Multiple Classifiers and Their
	Applications to Handwritten Digit Recognition, 
	MSc Thesis, Institute of Graduate Studies in Science and 
	Engineering, Bogazici University.

	E. Alpaydin, C. Kaynak (1998) Cascading Classifiers, Kybernetika,
	to appear. ftp://ftp.icsi.berkeley.edu/pub/ai/ethem/kyb.ps.Z

4. Relevant Information:
	We used preprocessing programs made available by NIST to extract
	normalized bitmaps of handwritten digits from a preprinted form. From
	a total of 43 people, 30 contributed to the training set and different
	13 to the test set. Inputs are centered and normalized as 32x32 bitmaps.

	In optdigits, Training, Validation and Writer-dependent sets are 
	combined to form one large training set and the Writer-independent set
	is the test set. 
	There to decrease dimensionality, 32x32 bitmaps are low-pass filtered 
	and undersampled to get 8x8 integer matrices and converted to UCI
	format. This optdigits-orig is in the original format following that 
	of NIST.

	For info on NIST preprocessing routines, see 
	M. D. Garris, J. L. Blue, G. T. Candela, D. L. Dimmick, J. Geist, 
	P. J. Grother, S. A. Janet, and C. L. Wilson, NIST Form-Based 
	Handprint Recognition System, NISTIR 5469, 1994.

5. Number of Instances
	optdigits-orig.tra	Training		1934
	optdigits-orig.cv	Validation		 946
	optdigits-orig.wdep	Writer-dependent	 943
	optdigits-orig.windep	Writer-independent	1797
	
	All files contain a header which include relevant information. See 
	NIST TR for details.

6. Number of Attributes
	1024 input+1 class attribute

7. For Each Attribute:
	All input attributes are integers in the range binary '0'/'1' with 
	'\n' at the end of each row to visualize input.
	The last attribute is the class code 0..9

8. Missing Attribute Values
	None

9. Class Distribution
			tra	cv	wdep	windep
	Class 0		189	 87	100	178
	Class 1		198	 97	 94	182
	Class 2		195	 92	 93	177
	Class 3		199	 85	105	183
	Class 4		186	114	 87	181
	Class 5		187	108	 81	182
	Class 6		195	 87	 95	181
	Class 7		201	 96	 90	179
	Class 8		180	 91	109	174
	Class 9		204	 89	 89	180
