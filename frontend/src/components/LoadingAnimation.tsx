const LoadingAnimation = () => {
  return (
    <div className="flex items-center justify-center h-full">
      <div
        className="spinner-border text-primary"
        role="status"
        style={{ display: 'block' }}
      >
        <span className="visually-hidden">Loading...</span>
      </div>
    </div>
  );
};

export default LoadingAnimation;
