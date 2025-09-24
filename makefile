.PHONY: clean

dst/change_me_output.gal: main.py solver.py planet.py
	python3 main.py Nbody/input_data/ellipse_N_00010.gal

run: dst/change_me_output.gal

compare: dst/change_me_output.gal dst/compiled
	./dst/compiled 10 dst/change_me_output.gal Nbody/ref_output_data/ellipse_N_00010_after200steps.gal

compile_comparator: dst/compiled

dst/compiled: Nbody/compare_gal_files/compare_gal_files.c
	gcc -lm Nbody/compare_gal_files/compare_gal_files.c -o dst/compiled

clean:
	rm -rf __pycache__
	rm -f dst/change_me_output.gal dst/compiled

2:
	python3 main.py Nbody/input_data/ellipse_N_00100.gal

2_compare:
	./dst/compiled 100 dst/change_me_output.gal Nbody/ref_output_data/ellipse_N_00100_after200steps.gal
