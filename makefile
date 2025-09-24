run:
	python3 main.py 10 Nbody/input_data/ellipse_N_00010.gal

compare:
	./dst/compiled 10 dst/change_me_output.gal Nbody/ref_output_data/ellipse_N_00010_after200steps.gal

compile_comparator:
	gcc -lm Nbody/compare_gal_files/compare_gal_files.c -o dst/compiled


2:
	python3 main.py 100 Nbody/input_data/ellipse_N_00100.gal

2_compare:
	./dst/compiled 100 dst/change_me_output.gal Nbody/ref_output_data/ellipse_N_00100_after200steps.gal
