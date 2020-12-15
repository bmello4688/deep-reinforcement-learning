& 'c:\ProgramData\Anaconda3\shell\condabin\conda-hook.ps1'
conda init powershell
conda env create
conda activate drlnd
python -m ipykernel install --user --name drlnd --display-name "drlnd"