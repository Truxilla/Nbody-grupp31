all: compare
.PHONY: clean

dst/%_out.gal: Nbody/input_data/%.gal main.py solver.py planet.py
	python3 main.py $< -o $@

dst/%.mp4: Nbody/input_data/%.gal main.py solver.py planet.py
	python3 main.py $< 1000 -a $@

compare:  dst/compiled dst/ellipse_N_00010_out.gal dst/ellipse_N_00100_out.gal dst/ellipse_N_00500_out.gal dst/ellipse_N_01000_out.gal dst/ellipse_N_02000_out.gal
	./dst/compiled 10 dst/ellipse_N_00010_out.gal Nbody/ref_output_data/ellipse_N_00010_after200steps.gal
	./dst/compiled 100 dst/ellipse_N_00100_out.gal Nbody/ref_output_data/ellipse_N_00100_after200steps.gal
	./dst/compiled 500 dst/ellipse_N_00500_out.gal Nbody/ref_output_data/ellipse_N_00500_after200steps.gal
	./dst/compiled 1000 dst/ellipse_N_01000_out.gal Nbody/ref_output_data/ellipse_N_01000_after200steps.gal
	./dst/compiled 2000 dst/ellipse_N_02000_out.gal Nbody/ref_output_data/ellipse_N_02000_after200steps.gal

dst/compiled: Nbody/compare_gal_files/compare_gal_files.c
	gcc -lm $^ -o $@

clean:
	rm -rf __pycache__
	rm -f dst/*_out.gal dst/compiled
